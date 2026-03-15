"""
Database migration script to add missing columns to the qr_codes and users tables.

This script checks for and adds any columns that are defined in the
QRCode and User models but missing from the database. This is needed for users
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
from models import db, QRCode, User


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


def _migrate_table(conn, inspector, table_name, model_class):
    """Add missing columns from the model to the given table."""
    if table_name not in inspector.get_table_names():
        print(f"Table '{table_name}' does not exist yet.")
        print("No migration needed - the database will be created with the correct schema.")
        return True

    existing_columns = {col['name'] for col in inspector.get_columns(table_name)}
    model_columns = {col.name: col for col in model_class.__table__.columns}
    missing = set(model_columns.keys()) - existing_columns

    if not missing:
        print(f"✓ Table '{table_name}': all columns present. No migration needed.")
        return True

    print(f"Table '{table_name}': found {len(missing)} missing column(s): {', '.join(sorted(missing))}")

    for col_name in sorted(missing):
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', col_name):
            print(f"  ✗ Skipping invalid column name: '{col_name}'")
            continue
        col = model_columns[col_name]
        sql_type = _get_column_sql_type(col)
        print(f"  Adding column '{col_name}' ({sql_type}) to '{table_name}'...")
        conn.execute(text(
            f"ALTER TABLE {table_name} ADD COLUMN {col_name} {sql_type}"
        ))

    # Verify
    inspector2 = inspect(db.engine)
    existing_after = {col['name'] for col in inspector2.get_columns(table_name)}
    still_missing = set(model_columns.keys()) - existing_after
    if still_missing:
        print(f"✗ Migration incomplete for '{table_name}'. Still missing: {', '.join(sorted(still_missing))}")
        return False

    print(f"✓ Table '{table_name}': migration successful.")
    return True


def migrate_database():
    """Add any missing columns to the qr_codes and users tables."""
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
            inspector = inspect(db.engine)
            with db.engine.connect() as conn:
                ok_qr = _migrate_table(conn, inspector, 'qr_codes', QRCode)
                ok_users = _migrate_table(conn, inspector, 'users', User)
                conn.commit()
            return ok_qr and ok_users

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
