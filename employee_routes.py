"""
Employee management routes for Flask application.
Import and register these routes in app.py
"""

def register_employee_routes(app, db, login_required, current_user, request, render_template, redirect, url_for, flash, abort):
    """Register employee management routes."""
    from employee_service import EmployeeService
    from employee_forms import EmployeeForm
    from models import Employee, Brand

    @app.route('/employees')
    @login_required
    def employee_directory():
        """Employee directory page."""
        # Get search parameters
        search = request.args.get('search', '')
        brand_filter = request.args.get('brand', '')
        department_filter = request.args.get('department', '')

        # Get all employees with filters
        employees = EmployeeService.search_employees(
            search=search,
            brand_id=brand_filter if brand_filter else None,
            department=department_filter if department_filter else None
        )

        # Get user's brands for filter dropdown
        brands = Brand.query.filter_by(user_id=current_user.id, is_active=True).all()

        # Get unique departments
        departments = db.session.query(Employee.department).filter(
            Employee.department.isnot(None),
            Employee.department != ''
        ).distinct().all()
        departments = [d[0] for d in departments if d[0]]

        return render_template('dashboard/employees.html',
                             employees=employees,
                             brands=brands,
                             departments=departments,
                             search=search,
                             brand_filter=brand_filter,
                             department_filter=department_filter)

    @app.route('/employees/create', methods=['GET', 'POST'])
    @login_required
    def employee_create():
        """Create employee profile."""
        form = EmployeeForm()

        # Populate brand choices
        brands = Brand.query.filter_by(user_id=current_user.id, is_active=True).all()
        form.brand_id.choices = [('', 'Select Brand')] + [(str(b.id), b.name) for b in brands]

        if form.validate_on_submit():
            try:
                # Handle profile image upload
                profile_image = None
                if form.profile_image.data:
                    profile_image = form.profile_image.data

                # Create employee
                employee = EmployeeService.create_employee(
                    user_id=current_user.id,
                    form_data={
                        'brand_id': int(form.brand_id.data) if form.brand_id.data else None,
                        'employee_id': form.employee_id.data,
                        'designation': form.designation.data,
                        'department': form.department.data,
                        'bio': form.bio.data,
                        'work_email': form.work_email.data,
                        'work_phone': form.work_phone.data,
                        'mobile': form.mobile.data,
                        'office_address': form.office_address.data,
                        'linkedin_url': form.linkedin_url.data,
                        'twitter_url': form.twitter_url.data,
                        'facebook_url': form.facebook_url.data,
                        'instagram_url': form.instagram_url.data,
                        'github_url': form.github_url.data,
                        'website_url': form.website_url.data,
                        'custom_primary_color': form.custom_primary_color.data,
                    },
                    profile_image=profile_image
                )

                flash('Employee profile created successfully!', 'success')

                # Show vCard profile link
                if employee.vcard_profile:
                    vcard_url = url_for('vcard_profile', slug=employee.vcard_profile.slug, _external=True)
                    flash(f'vCard Profile: {vcard_url}', 'info')

                return redirect(url_for('employee_directory'))
            except ValueError as e:
                flash(str(e), 'danger')
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating employee: {str(e)}', 'danger')

        return render_template('dashboard/employee_form.html', form=form, action='create')

    @app.route('/employees/<int:employee_id>/edit', methods=['GET', 'POST'])
    @login_required
    def employee_edit(employee_id):
        """Edit employee profile."""
        # Get employee
        employee = Employee.query.filter_by(id=employee_id, user_id=current_user.id).first_or_404()

        form = EmployeeForm(obj=employee)

        # Populate brand choices
        brands = Brand.query.filter_by(user_id=current_user.id, is_active=True).all()
        form.brand_id.choices = [('', 'Select Brand')] + [(str(b.id), b.name) for b in brands]

        if form.validate_on_submit():
            try:
                # Handle profile image upload
                profile_image = None
                if form.profile_image.data:
                    profile_image = form.profile_image.data

                # Update employee
                updated_employee = EmployeeService.update_employee(
                    employee_id=employee_id,
                    form_data={
                        'brand_id': int(form.brand_id.data) if form.brand_id.data else None,
                        'employee_id': form.employee_id.data,
                        'designation': form.designation.data,
                        'department': form.department.data,
                        'bio': form.bio.data,
                        'work_email': form.work_email.data,
                        'work_phone': form.work_phone.data,
                        'mobile': form.mobile.data,
                        'office_address': form.office_address.data,
                        'linkedin_url': form.linkedin_url.data,
                        'twitter_url': form.twitter_url.data,
                        'facebook_url': form.facebook_url.data,
                        'instagram_url': form.instagram_url.data,
                        'github_url': form.github_url.data,
                        'website_url': form.website_url.data,
                        'custom_primary_color': form.custom_primary_color.data,
                        'is_active': form.is_active.data,
                        'show_in_directory': form.show_in_directory.data,
                    },
                    profile_image=profile_image
                )

                flash('Employee profile updated successfully!', 'success')
                return redirect(url_for('employee_directory'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating employee: {str(e)}', 'danger')

        # Pre-populate form
        if request.method == 'GET':
            form.brand_id.data = str(employee.brand_id) if employee.brand_id else ''

        return render_template('dashboard/employee_form.html', form=form, action='edit', employee=employee)

    @app.route('/employees/<int:employee_id>/delete', methods=['POST'])
    @login_required
    def employee_delete(employee_id):
        """Delete employee profile."""
        try:
            EmployeeService.delete_employee(employee_id)
            flash('Employee profile deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting employee: {str(e)}', 'danger')

        return redirect(url_for('employee_directory'))

    @app.route('/employees/<int:employee_id>/toggle-status', methods=['POST'])
    @login_required
    def employee_toggle_status(employee_id):
        """Toggle employee active status."""
        employee = Employee.query.filter_by(id=employee_id, user_id=current_user.id).first_or_404()

        employee.is_active = not employee.is_active
        db.session.commit()

        status = 'activated' if employee.is_active else 'deactivated'
        flash(f'Employee profile {status} successfully!', 'success')
        return redirect(url_for('employee_directory'))
