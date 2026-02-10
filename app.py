"""
Main Flask application for IBQ QR Code Generator.
"""
import os
import secrets
from flask import Flask, render_template, redirect, url_for, flash, request, send_file, jsonify, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import generate_csrf
from urllib.parse import urlparse
from datetime import datetime, timedelta
from config import config
from models import db, User, QRCode, Template, AuditLog
from forms import (LoginForm, RegistrationForm, QRCodeGenerateForm, QRCodeEditForm,
                   TemplateForm, ProfileForm, ChangePasswordForm, AccountSettingsForm,
                   PasswordResetRequestForm, PasswordResetForm)
from utils import (generate_vcard, create_qr_code, create_qr_code_svg, save_qr_code, 
                   generate_filename, get_qr_code_base64, generate_qr_data)
from sqlalchemy import desc, func

# Constants
MAX_VCARD_FILENAME_LENGTH = 50
PUBLIC_TOKEN_LENGTH = 16

def create_app(config_name='default'):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if no users exist
        if User.query.count() == 0:
            admin = User(
                username='admin',
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                is_verified=True,
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create default templates
            default_templates = [
                Template(
                    user_id=1,
                    name='Professional Black',
                    description='Professional black and white design',
                    category='business',
                    is_default=True,
                    is_public=True,
                    foreground_color='#000000',
                    background_color='#FFFFFF'
                ),
                Template(
                    user_id=1,
                    name='Modern Blue',
                    description='Modern blue themed design',
                    category='business',
                    is_default=True,
                    is_public=True,
                    foreground_color='#0066CC',
                    background_color='#F0F8FF'
                ),
                Template(
                    user_id=1,
                    name='Elegant Purple',
                    description='Elegant purple design',
                    category='business',
                    is_default=True,
                    is_public=True,
                    foreground_color='#663399',
                    background_color='#F5F0FF'
                )
            ]
            
            for template in default_templates:
                db.session.add(template)
            
            db.session.commit()
            print("Default admin user created: username='admin', password='admin123'")
    
    # Context processor
    @app.context_processor
    def utility_processor():
        return {
            'app_name': app.config['APP_NAME'],
            'app_version': app.config['APP_VERSION'],
            'now': datetime.utcnow,
            'csrf_token': generate_csrf
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Helper function for audit logging
    def log_action(action, resource_type=None, resource_id=None, details=None, status='success'):
        if current_user.is_authenticated:
            log = AuditLog(
                user_id=current_user.id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')[:255],
                status=status
            )
            db.session.add(log)
            db.session.commit()
    
    # Helper function for file uploads
    def allowed_file(filename):
        """Check if the file extension is allowed."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
    def save_uploaded_image(file, prefix='contact_image'):
        """Save uploaded image with secure filename."""
        if file and allowed_file(file.filename):
            # Generate secure filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{prefix}_{secrets.token_urlsafe(16)}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return filename, filepath
        return None, None
    
    # Public routes (no authentication required)
    @app.route('/c/<token>')
    def contact_profile(token):
        """Public contact profile page."""
        qr_code = QRCode.query.filter_by(public_token=token).first_or_404()
        # Atomic update to avoid race conditions
        QRCode.query.filter_by(id=qr_code.id).update({'view_count': QRCode.view_count + 1})
        db.session.commit()
        return render_template('contact_profile.html', contact=qr_code)
    
    @app.route('/c/<token>/vcard')
    def download_vcard(token):
        """Download vCard file for adding to contacts."""
        qr_code = QRCode.query.filter_by(public_token=token).first_or_404()
        
        # Generate vCard content
        vcard_content = qr_code.qr_data
        
        # Sanitize filename for Content-Disposition header
        filename = qr_code.contact_name or "contact"
        # Remove or replace characters that could break the header
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = filename.replace(' ', '_')[:MAX_VCARD_FILENAME_LENGTH]
        if not filename:
            filename = "contact"
        
        # Create response with vCard content
        response = Response(vcard_content, mimetype='text/vcard')
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}.vcf"'
        
        # Atomic update to avoid race conditions
        QRCode.query.filter_by(id=qr_code.id).update({'download_count': QRCode.download_count + 1})
        db.session.commit()
        
        return response
    
    # Routes
    @app.route('/')
    def index():
        """Landing page."""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Login page."""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            # Find user by username or email
            user = User.query.filter(
                (User.username == form.username.data) | (User.email == form.username.data)
            ).first()
            
            if user is None or not user.check_password(form.password.data):
                log_action('login_failed', details=f"Username: {form.username.data}", status='failure')
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            
            # Check if account is locked
            if user.is_account_locked():
                flash('Account is locked due to too many failed login attempts. Please try again later.', 'danger')
                return redirect(url_for('login'))
            
            # Check if account is active
            if not user.is_active:
                flash('Account is disabled. Please contact support.', 'danger')
                return redirect(url_for('login'))
            
            # Reset failed login attempts
            user.failed_login_attempts = 0
            user.account_locked_until = None
            user.last_login = datetime.utcnow()
            user.last_login_ip = request.remote_addr
            db.session.commit()
            
            login_user(user, remember=form.remember_me.data)
            log_action('login', status='success')
            
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('dashboard')
            
            flash(f'Welcome back, {user.first_name or user.username}!', 'success')
            return redirect(next_page)
        
        return render_template('auth/login.html', form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Registration page."""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                is_active=True
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            log_action('register', 'user', user.id, status='success')
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('auth/register.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        """Logout."""
        log_action('logout', status='success')
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Dashboard home page."""
        # Get statistics
        total_qr_codes = QRCode.query.filter_by(user_id=current_user.id).count()
        
        # This month
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        qr_codes_this_month = QRCode.query.filter(
            QRCode.user_id == current_user.id,
            QRCode.created_at >= start_of_month
        ).count()
        
        # This week
        start_of_week = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        qr_codes_this_week = QRCode.query.filter(
            QRCode.user_id == current_user.id,
            QRCode.created_at >= start_of_week
        ).count()
        
        # Recent QR codes
        recent_qr_codes = QRCode.query.filter_by(user_id=current_user.id).order_by(
            desc(QRCode.created_at)
        ).limit(5).all()
        
        # Recent activities
        recent_activities = AuditLog.query.filter_by(user_id=current_user.id).order_by(
            desc(AuditLog.created_at)
        ).limit(10).all()
        
        return render_template('dashboard/home.html',
                             total_qr_codes=total_qr_codes,
                             qr_codes_this_month=qr_codes_this_month,
                             qr_codes_this_week=qr_codes_this_week,
                             recent_qr_codes=recent_qr_codes,
                             recent_activities=recent_activities)
    
    @app.route('/generate', methods=['GET', 'POST'])
    @login_required
    def generate_qr():
        """Generate QR code page."""
        form = QRCodeGenerateForm()
        
        # Populate template choices
        templates = Template.query.filter(
            (Template.user_id == current_user.id) | (Template.is_public == True)
        ).all()
        form.template_id.choices = [(0, 'No Template')] + [(t.id, t.name) for t in templates]
        
        if form.validate_on_submit():
            try:
                # Get QR code type
                qr_type = form.qr_type.data
                
                # Prepare form data dictionary
                form_data = {
                    'contact_name': form.contact_name.data,
                    'contact_email': form.contact_email.data,
                    'contact_phone': form.contact_phone.data,
                    'contact_website': form.contact_website.data,
                    'contact_company': form.contact_company.data,
                    'contact_title': form.contact_title.data,
                    'contact_address': form.contact_address.data,
                    'url': form.url.data,
                    'text_content': form.text_content.data,
                    'email_address': form.email_address.data,
                    'email_subject': form.email_subject.data,
                    'email_body': form.email_body.data,
                    'sms_phone': form.sms_phone.data,
                    'sms_message': form.sms_message.data,
                    'phone_number': form.phone_number.data,
                    'wifi_ssid': form.wifi_ssid.data,
                    'wifi_password': form.wifi_password.data,
                    'wifi_encryption': form.wifi_encryption.data,
                    'wifi_hidden': form.wifi_hidden.data,
                    'social_url': form.social_url.data,
                    'app_url': form.app_url.data,
                    'event_title': form.event_title.data,
                    'event_location': form.event_location.data,
                    'event_start': form.event_start.data,
                    'event_end': form.event_end.data,
                    'event_description': form.event_description.data,
                    'location_latitude': form.location_latitude.data,
                    'location_longitude': form.location_longitude.data,
                    'location_name': form.location_name.data
                }
                
                # Generate QR data based on type
                qr_data = generate_qr_data(qr_type, form_data)
                
                # Handle custom image upload for vCard
                custom_image_filename = None
                custom_image_path = None
                if qr_type == 'vcard' and form.contact_image.data:
                    custom_image_filename, custom_image_path = save_uploaded_image(
                        form.contact_image.data, 
                        prefix=f'contact_{current_user.id}'
                    )
                
                # Generate public token
                public_token = secrets.token_urlsafe(PUBLIC_TOKEN_LENGTH)
                
                # Create QR code record
                qr_code = QRCode(
                    user_id=current_user.id,
                    name=form.name.data,
                    description=form.description.data,
                    category=form.category.data,
                    contact_name=form.contact_name.data,
                    contact_email=form.contact_email.data,
                    contact_phone=form.contact_phone.data,
                    contact_website=form.contact_website.data,
                    contact_company=form.contact_company.data,
                    contact_title=form.contact_title.data,
                    contact_address=form.contact_address.data,
                    qr_data=qr_data,
                    qr_type=qr_type,
                    public_token=public_token,
                    template_id=form.template_id.data if form.template_id.data else None
                )
                
                # For vcard, generate profile URL; for others, use direct data
                if qr_type == 'vcard':
                    qr_code_data = url_for('contact_profile', token=public_token, _external=True)
                else:
                    qr_code_data = qr_data
                
                # Handle logo upload
                logo_path = None
                if form.logo.data:
                    from werkzeug.utils import secure_filename
                    logo_file = form.logo.data
                    # Sanitize the filename
                    safe_name = secure_filename(form.name.data)
                    logo_filename = generate_filename('logo_' + safe_name, 'png')
                    logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
                    logo_file.save(logo_path)
                
                # QR code settings
                settings = {
                    'size': form.size.data or 300,
                    'foreground_color': form.foreground_color.data or '#000000',
                    'background_color': form.background_color.data or '#FFFFFF',
                    'error_correction': form.error_correction.data or 'H',
                    'border': form.border.data or 4,
                    'logo_path': logo_path,
                    'qr_style': form.qr_style.data or 'square',
                    'gradient_enabled': form.gradient_enabled.data or False,
                    'gradient_color': form.gradient_color.data if form.gradient_enabled.data else None,
                    'gradient_type': form.gradient_type.data or 'linear',
                    'frame_style': form.frame_style.data or 'none',
                    'frame_text': form.frame_text.data if form.frame_style.data != 'none' else None,
                    'frame_color': form.frame_color.data or '#000000',
                    'eye_style': form.eye_style.data or 'square',
                    'data_style': form.data_style.data or 'square'
                }
                
                # Generate QR code
                file_format = form.file_format.data or 'png'
                
                # For vCard with custom image, we need to add the logo after generation
                if file_format == 'svg':
                    qr_img = create_qr_code_svg(qr_code_data, settings)
                else:
                    qr_img = create_qr_code(qr_code_data, settings, logo_path=custom_image_path if qr_type == 'vcard' else None)
                
                # Save to file
                filename = generate_filename(form.name.data, file_format)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_size = save_qr_code(qr_img, file_path, file_format)
                
                # Update QR code record with file information
                qr_code.filename = filename
                qr_code.file_path = file_path
                qr_code.file_format = file_format
                qr_code.file_size = file_size
                qr_code.size = settings['size']
                qr_code.foreground_color = settings['foreground_color']
                qr_code.background_color = settings['background_color']
                qr_code.error_correction = settings['error_correction']
                qr_code.border = settings['border']
                qr_code.logo_path = logo_path
                qr_code.qr_style = settings['qr_style']
                qr_code.gradient_enabled = settings['gradient_enabled']
                qr_code.gradient_color = settings['gradient_color']
                qr_code.gradient_type = settings['gradient_type']
                qr_code.frame_style = settings['frame_style']
                qr_code.frame_text = settings['frame_text']
                qr_code.frame_color = settings['frame_color']
                qr_code.eye_style = settings['eye_style']
                qr_code.data_style = settings['data_style']
                
                # Save custom image path if uploaded
                if custom_image_path:
                    qr_code.custom_image_path = custom_image_path
                
                db.session.add(qr_code)
                db.session.commit()
                
                log_action('generate_qr_code', 'qr_code', qr_code.id, status='success')
                flash('QR Code generated successfully!', 'success')
                return redirect(url_for('view_qr_code', qr_id=qr_code.id))
                
            except Exception as e:
                db.session.rollback()
                log_action('generate_qr_code', details=str(e), status='failure')
                flash(f'Error generating QR code: {str(e)}', 'danger')
        
        return render_template('dashboard/generate.html', form=form)
    
    @app.route('/my-qrcodes')
    @login_required
    def my_qr_codes():
        """My QR codes page."""
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        category = request.args.get('category', '', type=str)
        
        query = QRCode.query.filter_by(user_id=current_user.id)
        
        if search:
            query = query.filter(
                (QRCode.name.contains(search)) | 
                (QRCode.description.contains(search))
            )
        
        if category:
            query = query.filter_by(category=category)
        
        qr_codes = query.order_by(desc(QRCode.created_at)).paginate(
            page=page,
            per_page=app.config['ITEMS_PER_PAGE'],
            error_out=False
        )
        
        return render_template('dashboard/my_qrcodes.html', qr_codes=qr_codes, search=search, category=category)
    
    @app.route('/qrcode/<int:qr_id>')
    @login_required
    def view_qr_code(qr_id):
        """View QR code details."""
        qr_code = QRCode.query.filter_by(id=qr_id, user_id=current_user.id).first_or_404()
        qr_code.view_count += 1
        db.session.commit()
        return render_template('dashboard/view_qrcode.html', qr_code=qr_code)
    
    @app.route('/qrcode/<int:qr_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_qr_code(qr_id):
        """Edit QR code."""
        qr_code = QRCode.query.filter_by(id=qr_id, user_id=current_user.id).first_or_404()
        form = QRCodeEditForm(obj=qr_code)
        
        if form.validate_on_submit():
            qr_code.name = form.name.data
            qr_code.description = form.description.data
            qr_code.category = form.category.data
            qr_code.updated_at = datetime.utcnow()
            db.session.commit()
            
            log_action('edit_qr_code', 'qr_code', qr_code.id, status='success')
            flash('QR Code updated successfully!', 'success')
            return redirect(url_for('view_qr_code', qr_id=qr_code.id))
        
        return render_template('dashboard/edit_qrcode.html', form=form, qr_code=qr_code)
    
    @app.route('/qrcode/<int:qr_id>/delete', methods=['POST'])
    @login_required
    def delete_qr_code(qr_id):
        """Delete QR code."""
        qr_code = QRCode.query.filter_by(id=qr_id, user_id=current_user.id).first_or_404()
        
        # Delete file
        if qr_code.file_path and os.path.exists(qr_code.file_path):
            os.remove(qr_code.file_path)
        
        db.session.delete(qr_code)
        db.session.commit()
        
        log_action('delete_qr_code', 'qr_code', qr_id, status='success')
        flash('QR Code deleted successfully!', 'success')
        return redirect(url_for('my_qr_codes'))
    
    @app.route('/qrcode/<int:qr_id>/download')
    @login_required
    def download_qr_code(qr_id):
        """Download QR code file."""
        qr_code = QRCode.query.filter_by(id=qr_id, user_id=current_user.id).first_or_404()
        
        if not qr_code.file_path or not os.path.exists(qr_code.file_path):
            flash('QR Code file not found', 'danger')
            return redirect(url_for('my_qr_codes'))
        
        qr_code.download_count += 1
        db.session.commit()
        
        log_action('download_qr_code', 'qr_code', qr_code.id, status='success')
        return send_file(qr_code.file_path, as_attachment=True, download_name=qr_code.filename)
    
    @app.route('/uploads/<filename>')
    @login_required
    def uploaded_file(filename):
        """Serve uploaded QR code files."""
        from werkzeug.utils import secure_filename
        
        # Sanitize filename to prevent path traversal
        safe_filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        
        # Verify the file exists and is within the upload folder
        if not os.path.exists(file_path):
            return "File not found", 404
        
        # Verify the resolved path is within the upload folder (additional security)
        upload_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
        file_path = os.path.abspath(file_path)
        if not file_path.startswith(upload_folder):
            return "Invalid file path", 403
            
        return send_file(file_path)
    
    @app.route('/templates')
    @login_required
    def templates():
        """Templates page."""
        page = request.args.get('page', 1, type=int)
        user_templates = Template.query.filter_by(user_id=current_user.id).order_by(desc(Template.created_at)).all()
        public_templates = Template.query.filter_by(is_public=True).filter(Template.user_id != current_user.id).all()
        
        return render_template('dashboard/templates.html', 
                             user_templates=user_templates,
                             public_templates=public_templates)
    
    @app.route('/templates/create', methods=['GET', 'POST'])
    @login_required
    def create_template():
        """Create template."""
        form = TemplateForm()
        
        if form.validate_on_submit():
            template = Template(
                user_id=current_user.id,
                name=form.name.data,
                description=form.description.data,
                category=form.category.data,
                is_public=form.is_public.data,
                foreground_color=form.foreground_color.data,
                background_color=form.background_color.data,
                size=form.size.data,
                error_correction=form.error_correction.data,
                border=form.border.data
            )
            
            db.session.add(template)
            db.session.commit()
            
            log_action('create_template', 'template', template.id, status='success')
            flash('Template created successfully!', 'success')
            return redirect(url_for('templates'))
        
        return render_template('dashboard/create_template.html', form=form)
    
    @app.route('/templates/<int:template_id>/delete', methods=['POST'])
    @login_required
    def delete_template(template_id):
        """Delete template."""
        template = Template.query.filter_by(id=template_id, user_id=current_user.id).first_or_404()
        
        if template.is_default:
            flash('Cannot delete default templates', 'danger')
            return redirect(url_for('templates'))
        
        db.session.delete(template)
        db.session.commit()
        
        log_action('delete_template', 'template', template_id, status='success')
        flash('Template deleted successfully!', 'success')
        return redirect(url_for('templates'))
    
    @app.route('/settings/profile', methods=['GET', 'POST'])
    @login_required
    def settings_profile():
        """Profile settings."""
        form = ProfileForm(obj=current_user)
        
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.company = form.company.data
            current_user.phone = form.phone.data
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            
            log_action('update_profile', 'user', current_user.id, status='success')
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('settings_profile'))
        
        return render_template('dashboard/settings_profile.html', form=form)
    
    @app.route('/settings/account', methods=['GET', 'POST'])
    @login_required
    def settings_account():
        """Account settings."""
        form = AccountSettingsForm(obj=current_user)
        
        if form.validate_on_submit():
            current_user.theme = form.theme.data
            current_user.notifications_enabled = form.notifications_enabled.data
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            
            log_action('update_account_settings', 'user', current_user.id, status='success')
            flash('Account settings updated successfully!', 'success')
            return redirect(url_for('settings_account'))
        
        return render_template('dashboard/settings_account.html', form=form)
    
    @app.route('/settings/password', methods=['GET', 'POST'])
    @login_required
    def settings_password():
        """Change password."""
        form = ChangePasswordForm()
        
        if form.validate_on_submit():
            if not current_user.check_password(form.current_password.data):
                flash('Current password is incorrect', 'danger')
                return redirect(url_for('settings_password'))
            
            current_user.set_password(form.new_password.data)
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            
            log_action('change_password', 'user', current_user.id, status='success')
            flash('Password changed successfully!', 'success')
            return redirect(url_for('settings_account'))
        
        return render_template('dashboard/settings_password.html', form=form)
    
    @app.route('/settings/api-key')
    @login_required
    def settings_api_key():
        """API key settings."""
        return render_template('dashboard/settings_api_key.html')
    
    @app.route('/settings/api-key/generate', methods=['POST'])
    @login_required
    def generate_api_key():
        """Generate new API key."""
        current_user.generate_api_key()
        db.session.commit()
        
        log_action('generate_api_key', 'user', current_user.id, status='success')
        flash('New API key generated successfully!', 'success')
        return redirect(url_for('settings_api_key'))
    
    @app.route('/help')
    @login_required
    def help_page():
        """Help and support page."""
        return render_template('dashboard/help.html')
    
    @app.route('/help/faq')
    @login_required
    def faq():
        """FAQ page."""
        return render_template('dashboard/faq.html')
    
    @app.route('/help/documentation')
    @login_required
    def documentation():
        """Documentation page."""
        return render_template('dashboard/documentation.html')
    
    @app.route('/help/contact')
    @login_required
    def contact():
        """Contact support page."""
        return render_template('dashboard/contact.html')
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
