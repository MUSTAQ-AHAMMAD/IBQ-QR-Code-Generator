"""
Forms for employee management.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, URLField
from wtforms.validators import DataRequired, Email, Optional, URL, Length

class EmployeeForm(FlaskForm):
    """Form for creating and editing employees."""

    # Basic Information
    employee_id = StringField('Employee ID', validators=[Length(max=50)])
    designation = StringField('Job Title/Designation', validators=[DataRequired(), Length(max=100)])
    department = StringField('Department', validators=[Length(max=100)])

    # Profile
    profile_image = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    bio = TextAreaField('Bio', validators=[Length(max=500)])

    # Contact Information
    work_email = StringField('Work Email', validators=[Email(), Length(max=120)])
    work_phone = StringField('Work Phone', validators=[Length(max=20)])
    mobile = StringField('Mobile', validators=[Length(max=20)])
    office_address = TextAreaField('Office Address')

    # Social Links
    linkedin_url = URLField('LinkedIn URL', validators=[Optional(), URL(), Length(max=255)])
    twitter_url = URLField('Twitter URL', validators=[Optional(), URL(), Length(max=255)])
    facebook_url = URLField('Facebook URL', validators=[Optional(), URL(), Length(max=255)])
    instagram_url = URLField('Instagram URL', validators=[Optional(), URL(), Length(max=255)])
    github_url = URLField('GitHub URL', validators=[Optional(), URL(), Length(max=255)])
    website_url = URLField('Website URL', validators=[Optional(), URL(), Length(max=255)])

    # Brand Association
    brand_id = SelectField('Brand', coerce=int, validators=[Optional()])

    # Custom Branding (Optional Overrides)
    custom_primary_color = StringField('Custom Primary Color (Optional)', validators=[Length(max=7)])
    custom_qr_style = SelectField('Custom QR Style (Optional)',
                                  choices=[('', 'Use Brand Default'),
                                          ('square', 'Square'),
                                          ('rounded', 'Rounded'),
                                          ('dots', 'Dots'),
                                          ('circles', 'Circles')],
                                  validators=[Optional()])

    # Settings
    is_active = BooleanField('Active')
    show_in_directory = BooleanField('Show in Employee Directory')


class EmployeeSearchForm(FlaskForm):
    """Form for searching employees."""

    search = StringField('Search', validators=[Length(max=100)])
    department = SelectField('Department', choices=[('', 'All Departments')], validators=[Optional()])
    brand_id = SelectField('Brand', choices=[('', 'All Brands')], coerce=int, validators=[Optional()])
    is_active = SelectField('Status',
                           choices=[('', 'All'), ('active', 'Active Only'), ('inactive', 'Inactive Only')],
                           validators=[Optional()])
