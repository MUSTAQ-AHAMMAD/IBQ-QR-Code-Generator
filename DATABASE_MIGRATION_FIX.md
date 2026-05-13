# Database Migration Fix for brand_id Column Error

## Problem

You may encounter the following error when running the application:

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: qr_codes.brand_id
```

This error occurs because the database schema is out of sync with the models. The `Brand` model and `brand_id` foreign key were added to the codebase, but the database tables weren't updated.

## Solution

Follow these steps to fix the database schema:

### Option 1: Apply Migration (Recommended for existing databases)

If you have existing data that you want to preserve, use this option:

```bash
# 1. Make sure you're in the project root directory
cd /path/to/IBQ-QR-Code-Generator

# 2. Activate your virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate

# 3. Apply the migration to update the database schema
flask db upgrade
```

This will:
- Create the `brands` table
- Add the `brand_id` column to the `qr_codes` table
- Add the `company_logo` column to the `users` table

### Option 2: Recreate Database (For development/testing)

If you don't need to preserve existing data:

```bash
# 1. Delete the existing database file (SQLite)
# On Windows:
del instance\qr_generator.db
# On Unix/macOS:
rm instance/qr_generator.db

# 2. Run the application - it will recreate the database with the correct schema
python app.py
```

The application uses `db.create_all()` which will create all tables with the current schema.

### Option 3: Manual Database Update (Advanced)

If you need to manually update the database:

```sql
-- Create brands table
CREATE TABLE brands (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    website VARCHAR(200),
    email VARCHAR(120),
    phone VARCHAR(20),
    address TEXT,
    logo VARCHAR(255),
    primary_color VARCHAR(7),
    secondary_color VARCHAR(7),
    is_default BOOLEAN,
    is_active BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX ix_brands_user_id ON brands(user_id);

-- Add brand_id column to qr_codes table
ALTER TABLE qr_codes ADD COLUMN brand_id INTEGER;
CREATE INDEX ix_qr_codes_brand_id ON qr_codes(brand_id);

-- Add company_logo column to users table
ALTER TABLE users ADD COLUMN company_logo VARCHAR(255);
```

## Verifying the Fix

After applying the migration, verify the fix by:

1. Starting the application:
   ```bash
   python app.py
   ```

2. Logging in and accessing the dashboard at `http://localhost:5000/dashboard`

3. If no errors appear, the migration was successful!

## Understanding Database Migrations

This project uses Flask-Migrate (Alembic) for database schema management. When models are updated, you should create and apply migrations:

### Creating a New Migration

When you modify models in `models.py`:

```bash
# Create a migration script
flask db migrate -m "Description of your changes"

# Review the generated migration file in migrations/versions/
# Make any necessary adjustments

# Apply the migration
flask db upgrade
```

### Migration History

You can view the migration history:

```bash
# Show current migration version
flask db current

# Show migration history
flask db history
```

### Rolling Back Migrations

If needed, you can rollback to a previous version:

```bash
# Rollback one migration
flask db downgrade

# Rollback to a specific version
flask db downgrade <revision_id>
```

## Troubleshooting

### Error: "flask: command not found"

Make sure your virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Unix/macOS
source venv/bin/activate
```

### Error: "No migrations directory"

Initialize Flask-Migrate:
```bash
flask db init
```

### Migration conflicts

If you encounter conflicts, you may need to:
1. Backup your database
2. Recreate the migration: `flask db migrate -m "Your description"`
3. Review and apply: `flask db upgrade`

## Support

If you continue to experience issues:
1. Check that all dependencies are installed: `pip install -r requirements.txt`
2. Verify Flask-Migrate is installed: `pip show Flask-Migrate`
3. Create an issue on GitHub with the full error message
