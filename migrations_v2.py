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
            from sqlalchemy import inspect

            with db.engine.connect() as conn:
                inspector = inspect(db.engine)

                # Helper function to check if column exists
                def column_exists(table_name, column_name):
                    if table_name not in inspector.get_table_names():
                        return False
                    columns = [col['name'] for col in inspector.get_columns(table_name)]
                    return column_name in columns

                # Helper function to check if index exists
                def index_exists(table_name, index_name):
                    if table_name not in inspector.get_table_names():
                        return False
                    indexes = [idx['name'] for idx in inspector.get_indexes(table_name)]
                    return index_name in indexes

                # Brand table enhancements
                print("Enhancing brands table...")
                brand_migrations = [
                    ("organization_id", "ALTER TABLE brands ADD COLUMN organization_id INTEGER"),
                    ("slug", "ALTER TABLE brands ADD COLUMN slug VARCHAR(100)"),
                    ("favicon", "ALTER TABLE brands ADD COLUMN favicon VARCHAR(255)"),
                    ("background_color", "ALTER TABLE brands ADD COLUMN background_color VARCHAR(7) DEFAULT '#ffffff'"),
                    ("font_family", "ALTER TABLE brands ADD COLUMN font_family VARCHAR(100) DEFAULT 'Inter'"),
                    ("button_style", "ALTER TABLE brands ADD COLUMN button_style VARCHAR(50) DEFAULT 'rounded'"),
                    ("card_style", "ALTER TABLE brands ADD COLUMN card_style VARCHAR(50) DEFAULT 'shadow'"),
                    ("qr_style_preset", "ALTER TABLE brands ADD COLUMN qr_style_preset VARCHAR(50) DEFAULT 'modern'"),
                    ("employee_card_theme", "ALTER TABLE brands ADD COLUMN employee_card_theme JSON"),
                    ("landing_page_theme", "ALTER TABLE brands ADD COLUMN landing_page_theme JSON"),
                ]

                for col_name, sql in brand_migrations:
                    try:
                        if not column_exists('brands', col_name):
                            conn.execute(text(sql))
                            conn.commit()
                            print(f"  Added column: {col_name}")
                        else:
                            print(f"  Column already exists: {col_name}")
                    except Exception as e:
                        print(f"  Error adding column {col_name}: {e}")

                # User table enhancements
                print("Enhancing users table...")
                user_migrations = [
                    ("organization_id", "ALTER TABLE users ADD COLUMN organization_id INTEGER"),
                    ("role", "ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'"),
                ]

                for col_name, sql in user_migrations:
                    try:
                        if not column_exists('users', col_name):
                            conn.execute(text(sql))
                            conn.commit()
                            print(f"  Added column: {col_name}")
                        else:
                            print(f"  Column already exists: {col_name}")
                    except Exception as e:
                        print(f"  Error adding column {col_name}: {e}")

                # Add indexes
                print("Adding indexes...")
                indexes = [
                    ("brands", "idx_brands_slug", "CREATE INDEX idx_brands_slug ON brands(slug)"),
                    ("brands", "idx_brands_org", "CREATE INDEX idx_brands_org ON brands(organization_id)"),
                    ("users", "idx_users_org", "CREATE INDEX idx_users_org ON users(organization_id)"),
                    ("employees", "idx_employees_user", "CREATE INDEX idx_employees_user ON employees(user_id)"),
                    ("employees", "idx_employees_brand", "CREATE INDEX idx_employees_brand ON employees(brand_id)"),
                    ("qr_scans", "idx_qr_scans_timestamp", "CREATE INDEX idx_qr_scans_timestamp ON qr_scans(scan_timestamp)"),
                    ("vcard_profiles", "idx_vcard_profiles_slug", "CREATE INDEX idx_vcard_profiles_slug ON vcard_profiles(slug)"),
                    ("themes", "idx_themes_slug", "CREATE INDEX idx_themes_slug ON themes(slug)"),
                ]

                for table_name, idx_name, sql in indexes:
                    try:
                        if not index_exists(table_name, idx_name):
                            conn.execute(text(sql))
                            conn.commit()
                            print(f"  Created index: {idx_name}")
                        else:
                            print(f"  Index already exists: {idx_name}")
                    except Exception as e:
                        print(f"  Error creating index {idx_name}: {e}")

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
