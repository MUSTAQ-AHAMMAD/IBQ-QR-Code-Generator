"""
Database migrations for 100% requirements fulfillment.
This script adds new tables and enhances existing ones.
"""
from app import create_app
from models import db
from sqlalchemy import text

def run_migrations():
    """Run database migrations to add new tables and columns."""
    app = create_app()

    with app.app_context():
        print("Starting database migrations...")

        # Create all new tables
        print("Creating new tables (organizations, employees, vcard_profiles, qr_scans, themes, assets)...")
        db.create_all()

        # Add new columns to existing tables using raw SQL (for existing databases)
        try:
            with db.engine.connect() as conn:
                # Brand table enhancements
                print("Enhancing brands table...")
                brand_columns = [
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS organization_id INTEGER",
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS slug VARCHAR(100) UNIQUE",
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS favicon VARCHAR(255)",
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS background_color VARCHAR(7) DEFAULT '#ffffff'",
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS font_family VARCHAR(100) DEFAULT 'Inter'",
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS button_style VARCHAR(50) DEFAULT 'rounded'",
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS card_style VARCHAR(50) DEFAULT 'shadow'",
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS qr_style_preset VARCHAR(50) DEFAULT 'modern'",
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS employee_card_theme JSON",
                    "ALTER TABLE brands ADD COLUMN IF NOT EXISTS landing_page_theme JSON",
                ]

                for sql in brand_columns:
                    try:
                        conn.execute(text(sql))
                        conn.commit()
                    except Exception as e:
                        print(f"Column might already exist: {e}")

                # User table enhancements
                print("Enhancing users table...")
                user_columns = [
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS organization_id INTEGER",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'user'",
                ]

                for sql in user_columns:
                    try:
                        conn.execute(text(sql))
                        conn.commit()
                    except Exception as e:
                        print(f"Column might already exist: {e}")

                # Add indexes
                print("Adding indexes...")
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_brands_slug ON brands(slug)",
                    "CREATE INDEX IF NOT EXISTS idx_brands_org ON brands(organization_id)",
                    "CREATE INDEX IF NOT EXISTS idx_users_org ON users(organization_id)",
                    "CREATE INDEX IF NOT EXISTS idx_employees_user ON employees(user_id)",
                    "CREATE INDEX IF NOT EXISTS idx_employees_brand ON employees(brand_id)",
                    "CREATE INDEX IF NOT EXISTS idx_qr_scans_timestamp ON qr_scans(scan_timestamp)",
                    "CREATE INDEX IF NOT EXISTS idx_vcard_profiles_slug ON vcard_profiles(slug)",
                    "CREATE INDEX IF NOT EXISTS idx_themes_slug ON themes(slug)",
                ]

                for sql in indexes:
                    try:
                        conn.execute(text(sql))
                        conn.commit()
                    except Exception as e:
                        print(f"Index might already exist: {e}")

                # Generate slugs for existing brands
                print("Generating slugs for existing brands...")
                try:
                    from models import Brand
                    import re

                    brands = Brand.query.filter(Brand.slug.is_(None)).all()
                    for brand in brands:
                        slug = re.sub(r'[^\w\s-]', '', brand.name.lower())
                        slug = re.sub(r'[-\s]+', '-', slug)

                        # Ensure uniqueness
                        base_slug = slug
                        counter = 1
                        while Brand.query.filter_by(slug=slug).first():
                            slug = f"{base_slug}-{counter}"
                            counter += 1

                        brand.slug = slug

                    db.session.commit()
                    print(f"Generated slugs for {len(brands)} brands")
                except Exception as e:
                    print(f"Error generating slugs: {e}")
                    db.session.rollback()

        except Exception as e:
            print(f"Migration error: {e}")
            return False

        print("✅ Database migrations completed successfully!")
        return True

if __name__ == '__main__':
    run_migrations()
