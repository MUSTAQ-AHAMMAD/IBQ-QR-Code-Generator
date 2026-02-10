"""
Database models for the QR Code Generator application.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and user management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    company = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    email_verified_at = db.Column(db.DateTime)
    
    # Security
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))
    
    # Preferences
    theme = db.Column(db.String(10), default='light')
    notifications_enabled = db.Column(db.Boolean, default=True)
    
    # API
    api_key = db.Column(db.String(64), unique=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    qr_codes = db.relationship('QRCode', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    templates = db.relationship('Template', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
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

class QRCode(db.Model):
    """QR Code model for storing generated QR codes."""
    
    __tablename__ = 'qr_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
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
    
    # Template
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))
    
    # Statistics
    download_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def generate_public_token(self):
        """Generate a unique public token for the QR code profile URL."""
        self.public_token = secrets.token_urlsafe(16)
        return self.public_token
    
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
