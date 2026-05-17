"""
Database models for the QR Code Generator application.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

db = SQLAlchemy()

class Organization(db.Model):
    """Organization model for multi-tenant support."""

    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    domain = db.Column(db.String(255))  # Custom domain for organization
    subdomain = db.Column(db.String(100), unique=True)  # Subdomain for organization

    # Contact information
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    website = db.Column(db.String(200))

    # Settings
    is_active = db.Column(db.Boolean, default=True)
    max_users = db.Column(db.Integer, default=10)
    max_brands = db.Column(db.Integer, default=5)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = db.relationship('User', backref='organization', lazy='dynamic')
    brands = db.relationship('Brand', backref='organization', lazy='dynamic')

    def __repr__(self):
        return f'<Organization {self.name}>'

class Brand(db.Model):
    """Brand model for managing multiple brands per user/organization."""

    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True, index=True)

    # Brand information
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    website = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    # Branding customization
    logo = db.Column(db.String(255))  # Filename of uploaded brand logo
    favicon = db.Column(db.String(255))  # Filename of favicon
    primary_color = db.Column(db.String(7), default='#667eea')  # Primary brand color
    secondary_color = db.Column(db.String(7), default='#764ba2')  # Secondary brand color
    background_color = db.Column(db.String(7), default='#ffffff')  # Background color

    # Typography
    font_family = db.Column(db.String(100), default='Inter')  # Font family for brand

    # Style presets
    button_style = db.Column(db.String(50), default='rounded')  # rounded, square, pill
    card_style = db.Column(db.String(50), default='shadow')  # shadow, border, flat
    qr_style_preset = db.Column(db.String(50), default='modern')  # modern, classic, minimal

    # Theme configurations
    employee_card_theme = db.Column(db.JSON)  # JSON configuration for employee cards
    landing_page_theme = db.Column(db.JSON)  # JSON configuration for landing pages

    # Settings
    is_default = db.Column(db.Boolean, default=False)  # Default brand for user
    is_active = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    qr_codes = db.relationship('QRCode', backref='brand', lazy='dynamic', cascade='all, delete-orphan')
    employees = db.relationship('Employee', backref='brand', lazy='dynamic')

    def __repr__(self):
        return f'<Brand {self.name}>'

    def generate_slug(self):
        """Generate URL-safe slug from brand name."""
        import re
        slug = re.sub(r'[^\w\s-]', '', self.name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug

class User(UserMixin, db.Model):
    """User model for authentication and user management."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    company = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    # Role-Based Access Control (RBAC)
    role = db.Column(db.String(20), default='user')  # super_admin, admin, manager, employee, user

    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    email_verified_at = db.Column(db.DateTime)

    # Security
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))

    # Branding
    company_logo = db.Column(db.String(255))  # Filename of uploaded company logo
    user_photo = db.Column(db.String(255))  # Filename of uploaded user profile photo
    profile_color = db.Column(db.String(7), default='#667eea')  # Primary color for profile customization

    # Preferences
    theme = db.Column(db.String(10), default='light')
    notifications_enabled = db.Column(db.Boolean, default=True)

    # API
    api_key = db.Column(db.String(64), unique=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    brands = db.relationship('Brand', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    qr_codes = db.relationship('QRCode', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    templates = db.relationship('Template', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    employee_profile = db.relationship('Employee', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def generate_api_key(self):
        """Generate a new API key for the user."""
        self.api_key = secrets.token_urlsafe(48)
        return self.api_key
    
    def is_account_locked(self):
        """Check if the account is currently locked."""
        if self.account_locked_until and datetime.utcnow() < self.account_locked_until:
            return True
        return False
    
    def __repr__(self):
        return f'<User {self.username}>'

class Employee(db.Model):
    """Employee model for managing employees with vCard profiles."""

    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=True, index=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True, index=True)

    # Employee information
    employee_id = db.Column(db.String(50), unique=True)  # Company employee ID
    designation = db.Column(db.String(100))  # Job title
    department = db.Column(db.String(100))

    # Profile
    profile_image = db.Column(db.String(255))  # Employee profile photo
    bio = db.Column(db.Text)  # Short bio

    # Contact information
    work_email = db.Column(db.String(120))
    work_phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    office_address = db.Column(db.Text)

    # Social links
    linkedin_url = db.Column(db.String(255))
    twitter_url = db.Column(db.String(255))
    facebook_url = db.Column(db.String(255))
    instagram_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    website_url = db.Column(db.String(255))

    # Custom branding overrides (optional)
    custom_primary_color = db.Column(db.String(7))  # Override brand color
    custom_qr_style = db.Column(db.String(50))  # Override QR style
    custom_landing_theme = db.Column(db.JSON)  # Override landing page theme

    # Settings
    is_active = db.Column(db.Boolean, default=True)
    show_in_directory = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vcard_profile = db.relationship('VCardProfile', backref='employee', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Employee {self.employee_id}>'

class VCardProfile(db.Model):
    """VCard Profile model for public employee profile pages."""

    __tablename__ = 'vcard_profiles'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, unique=True, index=True)
    qr_code_id = db.Column(db.Integer, db.ForeignKey('qr_codes.id'), nullable=True)

    # Profile URL
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    public_token = db.Column(db.String(32), unique=True, index=True)

    # vCard data (VCF format)
    vcard_data = db.Column(db.Text)  # Complete vCard formatted data

    # Theme settings
    theme_mode = db.Column(db.String(10), default='light')  # light, dark, auto
    custom_css = db.Column(db.Text)  # Custom CSS for profile

    # Analytics
    view_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)
    last_viewed = db.Column(db.DateTime)

    # Settings
    is_public = db.Column(db.Boolean, default=True)
    allow_download = db.Column(db.Boolean, default=True)
    show_qr_code = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<VCardProfile {self.slug}>'

    def generate_slug(self, first_name, last_name):
        """Generate URL-safe slug from employee name."""
        import re
        name = f"{first_name}-{last_name}".lower()
        slug = re.sub(r'[^\w\s-]', '', name)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug

class QRScan(db.Model):
    """QR Scan model for tracking QR code scans with analytics."""

    __tablename__ = 'qr_scans'

    id = db.Column(db.Integer, primary_key=True)
    qr_code_id = db.Column(db.Integer, db.ForeignKey('qr_codes.id'), nullable=False, index=True)

    # Scan information
    scan_timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Device information
    device_type = db.Column(db.String(50))  # mobile, tablet, desktop
    operating_system = db.Column(db.String(50))  # iOS, Android, Windows, Mac, Linux
    browser = db.Column(db.String(50))  # Chrome, Safari, Firefox, etc.
    user_agent = db.Column(db.String(500))

    # Location information
    ip_address = db.Column(db.String(45))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Referrer information
    referrer_url = db.Column(db.String(500))
    referrer_domain = db.Column(db.String(255))

    # Tracking
    session_id = db.Column(db.String(64))  # Track repeat scans
    is_unique = db.Column(db.Boolean, default=True)  # First scan vs repeat

    def __repr__(self):
        return f'<QRScan {self.id} for QRCode {self.qr_code_id}>'

class Theme(db.Model):
    """Theme model for brand theme presets."""

    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)

    # Theme information
    name = db.Column(db.String(100), nullable=False)  # Corporate, Modern, Luxury, Minimal, Tech, Creative
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # preset, custom

    # Theme configuration (JSON structure)
    theme_config = db.Column(db.JSON, nullable=False)
    # Example structure:
    # {
    #   "colors": {
    #     "primary": "#667eea",
    #     "secondary": "#764ba2",
    #     "background": "#ffffff",
    #     "text": "#333333"
    #   },
    #   "typography": {
    #     "fontFamily": "Inter",
    #     "fontSize": "16px"
    #   },
    #   "buttons": {
    #     "style": "rounded",
    #     "shadow": true
    #   },
    #   "cards": {
    #     "style": "shadow",
    #     "radius": "12px"
    #   },
    #   "qr": {
    #     "style": "modern",
    #     "eyeStyle": "rounded",
    #     "dataStyle": "square"
    #   }
    # }

    # Preview
    preview_image = db.Column(db.String(255))  # Screenshot/preview of theme

    # Settings
    is_public = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)

    # Usage statistics
    usage_count = db.Column(db.Integer, default=0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Theme {self.name}>'

class Asset(db.Model):
    """Asset model for centralized media management."""

    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True, index=True)

    # Asset information
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))  # image, logo, favicon, profile, qr
    mime_type = db.Column(db.String(100))
    file_size = db.Column(db.Integer)  # Size in bytes

    # Image specific
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    thumbnail_path = db.Column(db.String(500))

    # Organization
    folder = db.Column(db.String(255))  # Virtual folder path
    tags = db.Column(db.JSON)  # Array of tags for organization

    # Usage tracking
    usage_count = db.Column(db.Integer, default=0)
    last_used = db.Column(db.DateTime)

    # Settings
    is_public = db.Column(db.Boolean, default=False)
    cdn_url = db.Column(db.String(500))  # CDN URL if uploaded to CDN

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Asset {self.filename}>'

class QRCode(db.Model):
    """QR Code model for storing generated QR codes."""

    __tablename__ = 'qr_codes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=True, index=True)  # Link to brand
    
    # QR Code information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    
    # Business card data
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    contact_website = db.Column(db.String(200))
    contact_company = db.Column(db.String(100))
    contact_address = db.Column(db.Text)
    contact_title = db.Column(db.String(100))
    
    # QR Code data
    qr_data = db.Column(db.Text, nullable=False)
    qr_type = db.Column(db.String(20), default='vcard')  # vcard, url, text, etc.
    public_token = db.Column(db.String(32), unique=True, index=True)  # Token for public profile URL
    
    # File information
    filename = db.Column(db.String(255))
    file_path = db.Column(db.String(500))
    file_format = db.Column(db.String(10), default='png')  # png, svg, pdf
    file_size = db.Column(db.Integer)
    
    # Customization
    size = db.Column(db.Integer, default=300)
    foreground_color = db.Column(db.String(7), default='#000000')
    background_color = db.Column(db.String(7), default='#FFFFFF')
    error_correction = db.Column(db.String(1), default='H')
    border = db.Column(db.Integer, default=4)
    logo_path = db.Column(db.String(500))
    custom_image_path = db.Column(db.String(500))
    
    # Advanced design options
    qr_style = db.Column(db.String(20), default='square')  # square, rounded, dots, circles
    gradient_enabled = db.Column(db.Boolean, default=False)
    gradient_color = db.Column(db.String(7))
    gradient_type = db.Column(db.String(20), default='linear')  # linear, radial
    frame_style = db.Column(db.String(20))  # none, basic, banner, bottom-text
    frame_text = db.Column(db.String(100))
    frame_color = db.Column(db.String(7), default='#000000')
    eye_style = db.Column(db.String(20), default='square')  # square, rounded, circle
    data_style = db.Column(db.String(20), default='square')  # square, rounded, circle, dot
    
    # Template
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))
    
    # Statistics
    download_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    scans = db.relationship('QRScan', backref='qr_code', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<QRCode {self.name}>'

class Template(db.Model):
    """Template model for QR code templates."""
    
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Template information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=False)
    is_default = db.Column(db.Boolean, default=False)
    
    # Template settings
    foreground_color = db.Column(db.String(7), default='#000000')
    background_color = db.Column(db.String(7), default='#FFFFFF')
    size = db.Column(db.Integer, default=300)
    error_correction = db.Column(db.String(1), default='H')
    border = db.Column(db.Integer, default=4)
    logo_path = db.Column(db.String(500))
    
    # Usage statistics
    usage_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    qr_codes = db.relationship('QRCode', backref='template', lazy='dynamic')
    
    def __repr__(self):
        return f'<Template {self.name}>'

class AuditLog(db.Model):
    """Audit log model for tracking user activities."""
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Action information
    action = db.Column(db.String(50), nullable=False)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    
    # Request information
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    
    # Status
    status = db.Column(db.String(20), default='success')  # success, failure, warning
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action} by User {self.user_id}>'
