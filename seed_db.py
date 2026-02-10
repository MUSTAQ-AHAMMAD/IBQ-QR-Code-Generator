"""
Database seeding script for the IBQ QR Code Generator.

Populates the database with sample data for development and testing.
This script should be run after init_db.py has created the tables.

Usage:
    python seed_db.py
"""
import sys
from datetime import datetime, timedelta
from config import config
from models import db, User, QRCode, Template, AuditLog

def get_app():
    """Create a minimal Flask app for database operations."""
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object(config['default'])
    db.init_app(app)
    return app

def seed_database():
    """Seed the database with sample data.

    Returns:
        True if successful, False otherwise.
    """
    app = get_app()

    with app.app_context():
        # Verify tables exist
        try:
            User.query.first()
        except Exception:
            print("✗ Database tables not found. Run 'python init_db.py' first.")
            return False

        # Check if sample data already exists
        if User.query.filter_by(username='demo').first():
            print("ℹ️  Sample data already exists. Skipping.")
            return True

        print("Creating sample users...")
        demo_user = User(
            username='demo',
            email='demo@example.com',
            first_name='Demo',
            last_name='User',
            company='Demo Corp',
            phone='+1-555-0100',
            is_verified=True,
            is_active=True,
            theme='light'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        db.session.flush()  # Get the user ID

        print("Creating sample templates...")
        sample_templates = [
            Template(
                user_id=demo_user.id,
                name='Corporate Green',
                description='Corporate green themed design for eco-friendly businesses',
                category='business',
                is_public=True,
                foreground_color='#2E7D32',
                background_color='#E8F5E9',
                size=300,
                error_correction='H',
                border=4
            ),
            Template(
                user_id=demo_user.id,
                name='Bold Red',
                description='Bold red design for high-impact marketing',
                category='marketing',
                is_public=True,
                foreground_color='#C62828',
                background_color='#FFEBEE',
                size=300,
                error_correction='H',
                border=4
            ),
        ]

        for template in sample_templates:
            db.session.add(template)

        print("Creating sample QR codes...")
        sample_qr_codes = [
            QRCode(
                user_id=demo_user.id,
                name='John Smith Business Card',
                description='Business card QR code for John Smith',
                category='business',
                contact_name='John Smith',
                contact_email='john.smith@democorp.com',
                contact_phone='+1-555-0101',
                contact_website='https://www.democorp.com',
                contact_company='Demo Corp',
                contact_title='Software Engineer',
                qr_data='BEGIN:VCARD\nVERSION:3.0\nN:Smith;John;;;\nFN:John Smith\nORG:Demo Corp\nTITLE:Software Engineer\nTEL;TYPE=WORK,VOICE:+1-555-0101\nEMAIL;TYPE=WORK,INTERNET:john.smith@democorp.com\nURL:https://www.democorp.com\nEND:VCARD',
                qr_type='vcard',
                foreground_color='#000000',
                background_color='#FFFFFF',
                size=300,
                error_correction='H',
                border=4,
                download_count=5,
                view_count=12,
                created_at=datetime.utcnow() - timedelta(days=7)
            ),
            QRCode(
                user_id=demo_user.id,
                name='Company Website',
                description='QR code linking to company website',
                category='marketing',
                qr_data='https://www.democorp.com',
                qr_type='url',
                foreground_color='#0066CC',
                background_color='#F0F8FF',
                size=300,
                error_correction='H',
                border=4,
                download_count=3,
                view_count=8,
                created_at=datetime.utcnow() - timedelta(days=3)
            ),
            QRCode(
                user_id=demo_user.id,
                name='WiFi Access',
                description='Guest WiFi access QR code',
                category='utility',
                qr_data='WIFI:T:WPA;S:DemoCorpGuest;P:welcome2024;;',
                qr_type='wifi',
                foreground_color='#2E7D32',
                background_color='#E8F5E9',
                size=300,
                error_correction='H',
                border=4,
                download_count=10,
                view_count=25,
                created_at=datetime.utcnow() - timedelta(days=1)
            ),
        ]

        for qr_code in sample_qr_codes:
            db.session.add(qr_code)

        print("Creating sample audit logs...")
        sample_logs = [
            AuditLog(
                user_id=demo_user.id,
                action='login',
                resource_type='user',
                resource_id=demo_user.id,
                details='User logged in successfully',
                ip_address='127.0.0.1',
                status='success',
                created_at=datetime.utcnow() - timedelta(days=7)
            ),
            AuditLog(
                user_id=demo_user.id,
                action='create_qr_code',
                resource_type='qr_code',
                resource_id=1,
                details='Created QR code: John Smith Business Card',
                ip_address='127.0.0.1',
                status='success',
                created_at=datetime.utcnow() - timedelta(days=7)
            ),
            AuditLog(
                user_id=demo_user.id,
                action='create_qr_code',
                resource_type='qr_code',
                resource_id=2,
                details='Created QR code: Company Website',
                ip_address='127.0.0.1',
                status='success',
                created_at=datetime.utcnow() - timedelta(days=3)
            ),
        ]

        for log in sample_logs:
            db.session.add(log)

        db.session.commit()
        print("✓ Sample users created.")
        print("✓ Sample templates created.")
        print("✓ Sample QR codes created.")
        print("✓ Sample audit logs created.")
        print()
        print("Sample login: username='demo', password='demo123'")

    return True

if __name__ == '__main__':
    print("=" * 60)
    print("IBQ QR Code Generator - Database Seeding")
    print("=" * 60)
    print()

    try:
        success = seed_database()
        print()
        if success:
            print("Database seeding completed successfully!")
        else:
            print("Database seeding failed.")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        sys.exit(1)

    print("=" * 60)
