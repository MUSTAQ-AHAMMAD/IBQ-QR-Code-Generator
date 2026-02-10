"""
Forms for the QR Code Generator application.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, URL
from models import User

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username or Email', validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """Registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    accept_terms = BooleanField('I accept the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username is already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class PasswordResetRequestForm(FlaskForm):
    """Password reset request form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class PasswordResetForm(FlaskForm):
    """Password reset form."""
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')

class QRCodeGenerateForm(FlaskForm):
    """QR Code generation form for all types."""
    name = StringField('QR Code Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    category = SelectField('Category', choices=[
        ('business', 'Business Card'),
        ('personal', 'Personal'),
        ('event', 'Event'),
        ('product', 'Product'),
        ('other', 'Other')
    ], validators=[Optional()])
    
    # QR Code Type Selection
    qr_type = SelectField('QR Code Type', choices=[
        ('vcard', 'Business Card / vCard'),
        ('url', 'Website URL'),
        ('text', 'Plain Text'),
        ('email', 'Email'),
        ('sms', 'SMS / Text Message'),
        ('phone', 'Phone Number'),
        ('wifi', 'WiFi Network'),
        ('facebook', 'Facebook Profile'),
        ('twitter', 'Twitter Profile'),
        ('instagram', 'Instagram Profile'),
        ('linkedin', 'LinkedIn Profile'),
        ('youtube', 'YouTube Channel'),
        ('app_store', 'App Store Link'),
        ('google_play', 'Google Play Store'),
        ('event', 'Calendar Event'),
        ('location', 'Location / Map')
    ], default='vcard', validators=[DataRequired()])
    
    # Business card fields (vcard)
    contact_name = StringField('Contact Name', validators=[Optional(), Length(max=100)])
    contact_email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    contact_phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    contact_website = StringField('Website', validators=[Optional(), Length(max=200)])
    contact_company = StringField('Company', validators=[Optional(), Length(max=100)])
    contact_title = StringField('Job Title', validators=[Optional(), Length(max=100)])
    contact_address = TextAreaField('Address', validators=[Optional(), Length(max=500)])
    
    # URL field
    url = StringField('URL', validators=[Optional(), Length(max=2000)])
    
    # Text field
    text_content = TextAreaField('Text Content', validators=[Optional(), Length(max=2000)])
    
    # Email fields
    email_address = StringField('Email Address', validators=[Optional(), Email(), Length(max=120)])
    email_subject = StringField('Email Subject', validators=[Optional(), Length(max=200)])
    email_body = TextAreaField('Email Body', validators=[Optional(), Length(max=1000)])
    
    # SMS fields
    sms_phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    sms_message = TextAreaField('Message', validators=[Optional(), Length(max=500)])
    
    # Phone field
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    
    # WiFi fields
    wifi_ssid = StringField('Network Name (SSID)', validators=[Optional(), Length(max=100)])
    wifi_password = StringField('Password', validators=[Optional(), Length(max=100)])
    wifi_encryption = SelectField('Security Type', choices=[
        ('WPA', 'WPA/WPA2'),
        ('WEP', 'WEP'),
        ('nopass', 'No Password')
    ], validators=[Optional()])
    wifi_hidden = BooleanField('Hidden Network')
    
    # Social Media fields
    social_url = StringField('Profile URL', validators=[Optional(), Length(max=500)])
    
    # App Store fields
    app_url = StringField('App Store URL', validators=[Optional(), Length(max=500)])
    
    # Event fields
    event_title = StringField('Event Title', validators=[Optional(), Length(max=200)])
    event_location = StringField('Event Location', validators=[Optional(), Length(max=200)])
    event_start = StringField('Start Date/Time', validators=[Optional()])
    event_end = StringField('End Date/Time', validators=[Optional()])
    event_description = TextAreaField('Event Description', validators=[Optional(), Length(max=1000)])
    
    # Location fields
    location_latitude = StringField('Latitude', validators=[Optional()])
    location_longitude = StringField('Longitude', validators=[Optional()])
    location_name = StringField('Location Name', validators=[Optional(), Length(max=200)])
    
    # QR Code customization
    size = IntegerField('QR Code Size (px)', validators=[Optional()], default=300)
    foreground_color = StringField('Foreground Color', validators=[Optional()], default='#000000')
    background_color = StringField('Background Color', validators=[Optional()], default='#FFFFFF')
    error_correction = SelectField('Error Correction', choices=[
        ('L', 'Low (7%)'),
        ('M', 'Medium (15%)'),
        ('Q', 'Quartile (25%)'),
        ('H', 'High (30%)')
    ], default='H')
    border = IntegerField('Border', validators=[Optional()], default=4)
    file_format = SelectField('File Format', choices=[
        ('png', 'PNG'),
        ('svg', 'SVG'),
        ('pdf', 'PDF')
    ], default='png')
    
    template_id = SelectField('Template', coerce=int, validators=[Optional()])
    
    submit = SubmitField('Generate QR Code')

class QRCodeEditForm(FlaskForm):
    """QR Code edit form."""
    name = StringField('QR Code Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    category = SelectField('Category', choices=[
        ('business', 'Business Card'),
        ('personal', 'Personal'),
        ('event', 'Event'),
        ('product', 'Product'),
        ('other', 'Other')
    ], validators=[Optional()])
    submit = SubmitField('Update QR Code')

class TemplateForm(FlaskForm):
    """Template creation/edit form."""
    name = StringField('Template Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    category = StringField('Category', validators=[Optional(), Length(max=50)])
    is_public = BooleanField('Make Public')
    
    # Template settings
    foreground_color = StringField('Foreground Color', validators=[Optional()], default='#000000')
    background_color = StringField('Background Color', validators=[Optional()], default='#FFFFFF')
    size = IntegerField('Size (px)', validators=[Optional()], default=300)
    error_correction = SelectField('Error Correction', choices=[
        ('L', 'Low'),
        ('M', 'Medium'),
        ('Q', 'Quartile'),
        ('H', 'High')
    ], default='H')
    border = IntegerField('Border', validators=[Optional()], default=4)
    
    submit = SubmitField('Save Template')

class ProfileForm(FlaskForm):
    """User profile edit form."""
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    """Change password form."""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    new_password2 = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')

class AccountSettingsForm(FlaskForm):
    """Account settings form."""
    theme = SelectField('Theme', choices=[
        ('light', 'Light'),
        ('dark', 'Dark')
    ])
    notifications_enabled = BooleanField('Enable Notifications')
    submit = SubmitField('Save Settings')
