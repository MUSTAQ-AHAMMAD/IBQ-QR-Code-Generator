"""
Employee service for managing employee operations.
"""
from models import db, Employee, VCardProfile, User, Brand
from werkzeug.utils import secure_filename
import secrets
import os

class EmployeeService:
    """Service for employee management operations."""

    @staticmethod
    def create_employee(user_id, form_data, profile_image=None):
        """
        Create a new employee profile.

        Args:
            user_id: ID of the user to create employee profile for
            form_data: Dictionary of form data
            profile_image: Uploaded file object (optional)

        Returns:
            Employee: Created employee object
        """
        # Check if employee profile already exists for this user
        existing = Employee.query.filter_by(user_id=user_id).first()
        if existing:
            raise ValueError("Employee profile already exists for this user")

        # Get user details
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        # Create employee
        employee = Employee(
            user_id=user_id,
            brand_id=form_data.get('brand_id'),
            organization_id=user.organization_id,
            employee_id=form_data.get('employee_id'),
            designation=form_data.get('designation'),
            department=form_data.get('department'),
            bio=form_data.get('bio'),
            work_email=form_data.get('work_email') or user.email,
            work_phone=form_data.get('work_phone'),
            mobile=form_data.get('mobile') or user.phone,
            office_address=form_data.get('office_address'),
            linkedin_url=form_data.get('linkedin_url'),
            twitter_url=form_data.get('twitter_url'),
            facebook_url=form_data.get('facebook_url'),
            instagram_url=form_data.get('instagram_url'),
            github_url=form_data.get('github_url'),
            website_url=form_data.get('website_url'),
            custom_primary_color=form_data.get('custom_primary_color'),
            custom_qr_style=form_data.get('custom_qr_style'),
            is_active=form_data.get('is_active', True),
            show_in_directory=form_data.get('show_in_directory', True)
        )

        # Handle profile image upload
        if profile_image:
            filename = EmployeeService._save_profile_image(profile_image, user_id)
            employee.profile_image = filename

        db.session.add(employee)
        db.session.flush()  # Get employee ID

        # Create VCard profile
        vcard_profile = EmployeeService._create_vcard_profile(employee, user)
        employee.vcard_profile = vcard_profile

        db.session.commit()

        return employee

    @staticmethod
    def update_employee(employee_id, form_data, profile_image=None):
        """Update an existing employee profile."""
        employee = Employee.query.get(employee_id)
        if not employee:
            raise ValueError("Employee not found")

        # Update fields
        employee.brand_id = form_data.get('brand_id')
        employee.employee_id = form_data.get('employee_id')
        employee.designation = form_data.get('designation')
        employee.department = form_data.get('department')
        employee.bio = form_data.get('bio')
        employee.work_email = form_data.get('work_email')
        employee.work_phone = form_data.get('work_phone')
        employee.mobile = form_data.get('mobile')
        employee.office_address = form_data.get('office_address')
        employee.linkedin_url = form_data.get('linkedin_url')
        employee.twitter_url = form_data.get('twitter_url')
        employee.facebook_url = form_data.get('facebook_url')
        employee.instagram_url = form_data.get('instagram_url')
        employee.github_url = form_data.get('github_url')
        employee.website_url = form_data.get('website_url')
        employee.custom_primary_color = form_data.get('custom_primary_color')
        employee.custom_qr_style = form_data.get('custom_qr_style')
        employee.is_active = form_data.get('is_active', True)
        employee.show_in_directory = form_data.get('show_in_directory', True)

        # Handle profile image upload
        if profile_image:
            filename = EmployeeService._save_profile_image(profile_image, employee.user_id)
            employee.profile_image = filename

        # Update VCard profile if it exists
        if employee.vcard_profile:
            EmployeeService._update_vcard_profile(employee)

        db.session.commit()

        return employee

    @staticmethod
    def delete_employee(employee_id):
        """Delete an employee profile."""
        employee = Employee.query.get(employee_id)
        if not employee:
            raise ValueError("Employee not found")

        # Delete profile image if exists
        if employee.profile_image:
            EmployeeService._delete_profile_image(employee.profile_image)

        db.session.delete(employee)
        db.session.commit()

    @staticmethod
    def get_employee_directory(filters=None, page=1, per_page=12):
        """
        Get paginated employee directory with filters.

        Args:
            filters: Dictionary of filter criteria
            page: Page number
            per_page: Items per page

        Returns:
            Pagination object
        """
        query = Employee.query.filter_by(show_in_directory=True, is_active=True)

        if filters:
            if filters.get('search'):
                search = f"%{filters['search']}%"
                query = query.join(User).filter(
                    db.or_(
                        User.first_name.ilike(search),
                        User.last_name.ilike(search),
                        Employee.designation.ilike(search),
                        Employee.department.ilike(search)
                    )
                )

            if filters.get('department'):
                query = query.filter_by(department=filters['department'])

            if filters.get('brand_id'):
                query = query.filter_by(brand_id=filters['brand_id'])

        return query.order_by(Employee.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def _save_profile_image(file, user_id):
        """Save uploaded profile image."""
        if not file:
            return None

        # Generate secure filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"employee_{user_id}_{secrets.token_hex(8)}.{ext}"

        # Save to uploads folder
        upload_folder = 'uploads/profiles'
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        return filename

    @staticmethod
    def _delete_profile_image(filename):
        """Delete profile image file."""
        if not filename:
            return

        filepath = os.path.join('uploads/profiles', filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    @staticmethod
    def _create_vcard_profile(employee, user):
        """Create VCard profile for employee."""
        # Generate slug from name
        slug = f"{user.first_name}-{user.last_name}".lower()
        slug = slug.replace(' ', '-')

        # Ensure uniqueness
        base_slug = slug
        counter = 1
        while VCardProfile.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Generate public token
        public_token = secrets.token_urlsafe(16)

        # Generate vCard data
        vcard_data = EmployeeService._generate_vcard_data(employee, user)

        vcard_profile = VCardProfile(
            employee_id=employee.id,
            slug=slug,
            public_token=public_token,
            vcard_data=vcard_data,
            is_public=True,
            allow_download=True,
            show_qr_code=True
        )

        db.session.add(vcard_profile)
        return vcard_profile

    @staticmethod
    def _update_vcard_profile(employee):
        """Update VCard profile data."""
        if not employee.vcard_profile:
            return

        user = User.query.get(employee.user_id)
        vcard_data = EmployeeService._generate_vcard_data(employee, user)
        employee.vcard_profile.vcard_data = vcard_data

    @staticmethod
    def _generate_vcard_data(employee, user):
        """Generate vCard 3.0 format data."""
        lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{user.first_name} {user.last_name}",
            f"N:{user.last_name};{user.first_name};;;",
        ]

        if employee.designation:
            lines.append(f"TITLE:{employee.designation}")

        if user.company or (employee.brand_id and employee.brand):
            org = employee.brand.name if employee.brand else user.company
            lines.append(f"ORG:{org}")

        if employee.work_email:
            lines.append(f"EMAIL;TYPE=WORK:{employee.work_email}")

        if employee.work_phone:
            lines.append(f"TEL;TYPE=WORK:{employee.work_phone}")

        if employee.mobile:
            lines.append(f"TEL;TYPE=CELL:{employee.mobile}")

        if employee.office_address:
            lines.append(f"ADR;TYPE=WORK:;;{employee.office_address};;;;")

        if employee.website_url:
            lines.append(f"URL:{employee.website_url}")

        lines.append("END:VCARD")

        return "\n".join(lines)

    @staticmethod
    def get_departments():
        """Get list of unique departments."""
        departments = db.session.query(Employee.department).distinct().filter(
            Employee.department.isnot(None),
            Employee.department != ''
        ).all()
        return [dept[0] for dept in departments]
