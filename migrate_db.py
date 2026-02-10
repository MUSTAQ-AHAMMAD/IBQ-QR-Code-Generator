"""
Database migration script to add missing custom_image_path column.

This script adds the custom_image_path column to the qr_codes table
if it doesn't already exist. This is needed for users upgrading from
older versions of the application.

Usage:
    python migrate_db.py
"""
import os
import sqlite3
from config import config

def migrate_database():
    """Add custom_image_path column to qr_codes table if it doesn't exist."""
    # Get database URI from config
    db_uri = config['default'].SQLALCHEMY_DATABASE_URI
    
    # Extract database file path from URI
    if db_uri.startswith('sqlite:///'):
        db_path = db_uri.replace('sqlite:///', '')
    else:
        print(f"Error: This migration script only supports SQLite databases.")
        print(f"Current database URI: {db_uri}")
        return False
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        print("No migration needed - the database will be created with the correct schema.")
        return True
    
    print(f"Migrating database: {db_path}")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if custom_image_path column exists
        cursor.execute("PRAGMA table_info(qr_codes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'custom_image_path' in columns:
            print("✓ Column 'custom_image_path' already exists. No migration needed.")
            conn.close()
            return True
        
        # Add the missing column
        print("Adding 'custom_image_path' column to qr_codes table...")
        cursor.execute("ALTER TABLE qr_codes ADD COLUMN custom_image_path VARCHAR(500)")
        conn.commit()
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(qr_codes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'custom_image_path' in columns:
            print("✓ Migration successful! Column 'custom_image_path' has been added.")
            conn.close()
            return True
        else:
            print("✗ Migration failed! Column was not added.")
            conn.close()
            return False
            
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
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
