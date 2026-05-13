"""
Database migration script to add brands table and update QR codes with brand_id.
Run this script to migrate your existing database to support the new brand system.
"""
import os
from app import create_app
from models import db, Brand, QRCode, User

def migrate_brands():
    """Add brands table and migrate existing QR codes."""
    app = create_app('development')

    with app.app_context():
        print("Starting brands migration...")

        # Create tables if they don't exist
        db.create_all()
        print("✓ Tables created/verified")

        # Check if brands table exists by trying to query it
        try:
            Brand.query.first()
            print("✓ Brands table exists")
        except Exception as e:
            print(f"✗ Error checking brands table: {e}")
            print("Please ensure the database schema has been updated")
            return

        # Create default brands for existing users who don't have any
        users = User.query.all()
        for user in users:
            existing_brand = Brand.query.filter_by(user_id=user.id).first()

            if not existing_brand:
                # Create default brand from user's company information
                brand_name = user.company or f"{user.first_name or user.username}'s Brand"

                default_brand = Brand(
                    user_id=user.id,
                    name=brand_name,
                    email=user.email,
                    phone=user.phone,
                    logo=user.company_logo,
                    primary_color=user.profile_color or '#667eea',
                    secondary_color='#764ba2',
                    is_default=True,
                    is_active=True
                )

                db.session.add(default_brand)
                db.session.flush()  # Get the brand ID

                # Update existing QR codes to link to this brand
                qr_codes = QRCode.query.filter_by(user_id=user.id, brand_id=None).all()
                for qr_code in qr_codes:
                    qr_code.brand_id = default_brand.id

                print(f"✓ Created default brand for user {user.username} and linked {len(qr_codes)} QR codes")

        db.session.commit()
        print("\n✓ Migration completed successfully!")
        print("All users now have a default brand, and existing QR codes have been linked to it.")

if __name__ == '__main__':
    migrate_brands()
