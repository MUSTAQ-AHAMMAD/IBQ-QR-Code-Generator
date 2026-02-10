"""
Database migration script to add missing custom_image_path column.

This script adds the custom_image_path column to the qr_codes table
if it doesn't already exist. This is needed for users upgrading from
older versions of the application.

Supports all database backends configured via DATABASE_URL (SQLite,
PostgreSQL, MySQL, etc.) using SQLAlchemy.

Usage:
    python migrate_db.py
"""
from flask import Flask
from sqlalchemy import inspect, text
from config import config
from models import db


def get_app():
    """Create a minimal Flask app for database operations."""
    app = Flask(__name__)
    app.config.from_object(config['default'])
    db.init_app(app)
    return app


def migrate_database():
    """Add custom_image_path column to qr_codes table if it doesn't exist."""
    try:
        app = get_app()
    except Exception as e:
        print(f"✗ Failed to initialize database connection: {e}")
        print("Please ensure the required database driver is installed.")
        print("For PostgreSQL: pip install psycopg2-binary")
        print("For MySQL: pip install mysqlclient")
        return False

    with app.app_context():
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"Database URI: {db_uri}")

        try:
            # Use SQLAlchemy inspector to check existing columns
            inspector = inspect(db.engine)

            # Check if qr_codes table exists
            if 'qr_codes' not in inspector.get_table_names():
                print("Table 'qr_codes' does not exist yet.")
                print("No migration needed - the database will be created with the correct schema.")
                return True

            # Check if custom_image_path column exists
            columns = [col['name'] for col in inspector.get_columns('qr_codes')]

            if 'custom_image_path' in columns:
                print("✓ Column 'custom_image_path' already exists. No migration needed.")
                return True

            # Add the missing column
            print("Adding 'custom_image_path' column to qr_codes table...")
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE qr_codes ADD COLUMN custom_image_path VARCHAR(500)"))
                conn.commit()

            # Verify the column was added
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('qr_codes')]

            if 'custom_image_path' in columns:
                print("✓ Migration successful! Column 'custom_image_path' has been added.")
                return True
            else:
                print("✗ Migration failed! Column was not added.")
                return False

        except Exception as e:
            print(f"✗ Database error: {e}")
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("QR Code Generator - Database Migration")
    print("=" * 60)
    print()
    
    success = migrate_database()
    
    print()
    if success:
        print("Migration completed successfully!")
        print("You can now run the application with: python app.py")
    else:
        print("Migration failed. Please check the error messages above.")
    print("=" * 60)
