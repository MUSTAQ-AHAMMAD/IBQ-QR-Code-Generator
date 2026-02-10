"""
Database migration script to add missing columns to the qr_codes table.

This script checks for and adds any columns that are defined in the
QRCode model but missing from the database. This is needed for users
upgrading from older versions of the application.

Supports all database backends configured via DATABASE_URL (SQLite,
PostgreSQL, MySQL, etc.) using SQLAlchemy.

Usage:
    python migrate_db.py
"""
from flask import Flask
from sqlalchemy import inspect, text
import re
from config import config
from models import db, QRCode


def get_app():
    """Create a minimal Flask app for database operations."""
    app = Flask(__name__)
    app.config.from_object(config['default'])
    db.init_app(app)
    return app


def _get_column_sql_type(column):
    """Return the SQL type string for a SQLAlchemy model column."""
    col_type = type(column.type)
    if col_type.__name__ == 'String':
        length = getattr(column.type, 'length', None)
        if length is not None:
            return f"VARCHAR({length})"
        return "TEXT"
    elif col_type.__name__ == 'Text':
        return "TEXT"
    elif col_type.__name__ == 'Integer':
        return "INTEGER"
    elif col_type.__name__ == 'Boolean':
        return "BOOLEAN"
    elif col_type.__name__ == 'DateTime':
        return "DATETIME"
    print(f"  ⚠ Unknown column type '{col_type.__name__}' for column '{column.name}', defaulting to TEXT")
    return "TEXT"


def migrate_database():
    """Add any missing columns to the qr_codes table."""
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

            # Get existing columns in the database
            existing_columns = {col['name'] for col in inspector.get_columns('qr_codes')}

            # Get expected columns from the QRCode model
            model_columns = {col.name: col for col in QRCode.__table__.columns}

            # Find missing columns
            missing = set(model_columns.keys()) - existing_columns

            if not missing:
                print("✓ All columns are present. No migration needed.")
                return True

            print(f"Found {len(missing)} missing column(s): {', '.join(sorted(missing))}")

            # Add each missing column
            with db.engine.connect() as conn:
                for col_name in sorted(missing):
                    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', col_name):
                        print(f"  ✗ Skipping invalid column name: '{col_name}'")
                        continue
                    col = model_columns[col_name]
                    sql_type = _get_column_sql_type(col)
                    print(f"  Adding column '{col_name}' ({sql_type})...")
                    conn.execute(text(
                        f"ALTER TABLE qr_codes ADD COLUMN {col_name} {sql_type}"
                    ))
                conn.commit()

            # Verify all columns were added
            inspector = inspect(db.engine)
            existing_columns = {col['name'] for col in inspector.get_columns('qr_codes')}
            still_missing = set(model_columns.keys()) - existing_columns

            if not still_missing:
                print("✓ Migration successful! All missing columns have been added.")
                return True
            else:
                print(f"✗ Migration incomplete. Still missing: {', '.join(sorted(still_missing))}")
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
