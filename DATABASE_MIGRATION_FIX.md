# Database Migration Fix for brand_id Column Error

## Problem

You may encounter the following error when running the application:

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: qr_codes.brand_id
```

This error occurs because the database schema is out of sync with the models. The `Brand` model and `brand_id` foreign key were added to the codebase, but the database tables weren't updated.

## Solution

Follow these steps to fix the database schema:

### Option 1: Recreate Database (Recommended for Development)

If you don't need to preserve existing data, this is the simplest solution:

```bash
# 1. Make sure you're in the project root directory
cd /path/to/IBQ-QR-Code-Generator

# 2. Delete the existing database file (SQLite)
# On Windows:
del instance\qr_generator.db
# On Unix/macOS:
rm instance/qr_generator.db

# 3. Delete the alembic_version table tracking file if it exists
rm -rf migrations/versions/__pycache__

# 4. Run the application - it will recreate the database with the correct schema
python app.py
```

The application uses `db.create_all()` which will create all tables with the current schema, including the `brands` table and `brand_id` column.

### Option 2: Apply Migration (For Existing Databases with Data)

If you have existing data that you want to preserve:

#### Step 1: Initialize or Reset Migration Tracking

First, we need to tell Alembic which migration version your database is at:

```bash
# 1. Activate your virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate

# 2. If you created the database with db.create_all() (not migrations),
# you need to stamp it with the initial migration version
flask db stamp head

# 3. Now apply any pending migrations
flask db upgrade
```

#### Step 2: Verify the Fix

After applying migrations, verify by starting the application:

```bash
python app.py
```

Then log in and access the dashboard at `http://localhost:5000/dashboard`. If no errors appear, the migration was successful!

### Option 3: Manual Database Update (Advanced)

If you need to manually update the database, you can use SQLite commands:

```bash
# 1. Open the database with sqlite3
sqlite3 instance/qr_generator.db

# 2. Run these SQL commands:
```

```sql
-- Create brands table
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    website VARCHAR(200),
    email VARCHAR(120),
    phone VARCHAR(20),
    address TEXT,
    logo VARCHAR(255),
    primary_color VARCHAR(7) DEFAULT '#667eea',
    secondary_color VARCHAR(7) DEFAULT '#764ba2',
    is_default BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS ix_brands_user_id ON brands(user_id);

-- Add brand_id column to qr_codes table (only if it doesn't exist)
-- Note: SQLite doesn't support ALTER TABLE ADD COLUMN IF NOT EXISTS directly
-- Check first if column exists
PRAGMA table_info(qr_codes);

-- If brand_id doesn't exist, add it:
ALTER TABLE qr_codes ADD COLUMN brand_id INTEGER;
CREATE INDEX IF NOT EXISTS ix_qr_codes_brand_id ON qr_codes(brand_id);

-- Add user photo and profile color columns if they don't exist
ALTER TABLE users ADD COLUMN company_logo VARCHAR(255);
ALTER TABLE users ADD COLUMN user_photo VARCHAR(255);
ALTER TABLE users ADD COLUMN profile_color VARCHAR(7) DEFAULT '#667eea';

-- Exit sqlite3
.quit
```

## Understanding Database Migrations

This project uses Flask-Migrate (Alembic) for database schema management.

### Migration Files

The migration in `migrations/versions/29c2fde25c94_initial_migration_create_all_tables.py` now includes:
- All tables (users, brands, templates, qr_codes, audit_logs)
- All columns including brand_id, company_logo, user_photo, and profile_color
- All indexes and foreign keys

Previous incremental migration files have been marked as obsolete since their changes are now included in the initial migration.

### For New Installations

New installations will automatically have the correct schema when running:
```bash
python app.py
```

The app creates all tables via `db.create_all()` on first run.

### For Existing Installations

Existing installations should use Option 1 (recreate) or Option 2 (apply migration) above.

## Troubleshooting

### Error: "flask: command not found"

Make sure your virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Unix/macOS
source venv/bin/activate
```

### Error: "Can't locate revision identified by 'head'"

This means Alembic can't find the migration history. Use Option 1 (recreate database):
```bash
rm instance/qr_generator.db
python app.py
```

### Database is locked

If you get a "database is locked" error:
1. Close all applications that might be using the database
2. Stop the Flask application
3. Try the operation again

### Migration conflicts

If you encounter migration conflicts:
1. Backup your database: `cp instance/qr_generator.db instance/qr_generator.db.backup`
2. Use Option 1 to recreate the database (you'll lose data)
3. Or manually fix the schema using Option 3

## Prevention

To prevent this issue in the future:

1. **Always use migrations** when modifying models:
   ```bash
   # After modifying models.py
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```

2. **Don't mix db.create_all() with migrations** - Choose one approach:
   - For production: Always use migrations
   - For development: db.create_all() is fine if you recreate often

3. **Version control your migrations** - Always commit migration files to git

## Support

If you continue to experience issues:
1. Check that all dependencies are installed: `pip install -r requirements.txt`
2. Verify Flask-Migrate is installed: `pip show Flask-Migrate`
3. Try the simplest solution first (Option 1: Recreate Database)
4. Create an issue on GitHub with the full error message and steps you've tried
