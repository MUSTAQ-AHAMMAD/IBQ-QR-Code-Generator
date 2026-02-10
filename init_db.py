"""
Database initialization script for the IBQ QR Code Generator.

Creates all database tables and sets up the default admin user
and default templates. This script can be run independently
of the main application.

Usage:
    python init_db.py
    python init_db.py --drop   # Drop all tables before recreating
"""
import sys
from config import config
from models import db, User, Template

def get_app():
    """Create a minimal Flask app for database operations."""
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object(config['default'])
    db.init_app(app)
    return app

def init_database(drop_existing=False):
    """Initialize the database with tables and default data.

    Args:
        drop_existing: If True, drop all existing tables before recreating.

    Returns:
        True if successful, False otherwise.
    """
    app = get_app()

    with app.app_context():
        if drop_existing:
            print("Dropping all existing tables...")
            db.drop_all()
            print("✓ All tables dropped.")

        print("Creating database tables...")
        db.create_all()
        print("✓ All tables created successfully.")

        # Create default admin user if no users exist
        if User.query.count() == 0:
            print("Creating default admin user...")
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
            print("Creating default templates...")
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
            print("✓ Default admin user created (username='admin', password='admin123').")
            print("✓ Default templates created.")
            print()
            print("⚠️  Change the default admin password immediately after first login!")
        else:
            print("ℹ️  Users already exist. Skipping default data creation.")

    return True

if __name__ == '__main__':
    print("=" * 60)
    print("IBQ QR Code Generator - Database Initialization")
    print("=" * 60)
    print()

    drop_existing = '--drop' in sys.argv

    if drop_existing:
        print("⚠️  WARNING: This will drop all existing tables and data!")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Aborted.")
            sys.exit(0)

    try:
        success = init_database(drop_existing=drop_existing)
        print()
        if success:
            print("Database initialization completed successfully!")
            print("You can now run the application with: python app.py")
        else:
            print("Database initialization failed.")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        sys.exit(1)

    print("=" * 60)
