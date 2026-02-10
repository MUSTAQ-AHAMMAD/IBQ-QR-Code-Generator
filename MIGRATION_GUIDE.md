# Database Migration Guide

## Overview

This guide helps you fix database schema issues that may occur when upgrading the IBQ QR Code Generator application.

## Common Issues

### Issue: "no such column: qr_codes.custom_image_path"

**Symptoms:**
- Dashboard and other pages not accessible
- Error message: `sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: qr_codes.custom_image_path`
- Application crashes when trying to query QR codes

**Cause:**
This error occurs when your database schema is outdated and missing the `custom_image_path` column. This typically happens when:
- You're upgrading from an older version of the application
- The database was created before the column was added to the model
- The database wasn't properly migrated during an upgrade

**Solution:**
Run the migration script to add the missing column to your database.

## Running the Migration Script

### Step 1: Backup Your Database (Recommended)

Before running any migration, it's good practice to backup your database:

**On Windows:**
```bash
# Backup the database file
copy instance\qrcode_generator.db instance\qrcode_generator.db.backup
```

**On Linux/Mac:**
```bash
# Backup the database file
cp instance/qrcode_generator.db instance/qrcode_generator.db.backup
```

### Step 2: Run the Migration

Execute the migration script:

```bash
python migrate_db.py
```

**Expected Output:**

If the column is missing, you'll see:
```
============================================================
QR Code Generator - Database Migration
============================================================

Migrating database: instance/qrcode_generator.db
Adding 'custom_image_path' column to qr_codes table...
✓ Migration successful! Column 'custom_image_path' has been added.

Migration completed successfully!
You can now run the application with: python app.py
============================================================
```

If the column already exists:
```
============================================================
QR Code Generator - Database Migration
============================================================

Migrating database: instance/qrcode_generator.db
✓ Column 'custom_image_path' already exists. No migration needed.

Migration completed successfully!
You can now run the application with: python app.py
============================================================
```

If no database exists yet:
```
============================================================
QR Code Generator - Database Migration
============================================================

Database file not found in any of these locations:
  - qrcode_generator.db
  - instance/qrcode_generator.db
No migration needed - the database will be created with the correct schema.

Migration completed successfully!
You can now run the application with: python app.py
============================================================
```

### Step 3: Start the Application

After the migration completes successfully, start the application:

```bash
python app.py
```

The application should now work without errors.

## What the Migration Script Does

The `migrate_db.py` script:

1. **Locates your database** - Checks both the root directory and the `instance/` folder (Flask's default location)
2. **Checks if migration is needed** - Verifies if the `custom_image_path` column already exists
3. **Adds missing column** - If the column is missing, adds it to the `qr_codes` table
4. **Is safe to run multiple times** - The script is idempotent, meaning it won't cause issues if run more than once

## Database Locations

The application may store the database in different locations depending on your setup:

- **Default (Flask instance folder):** `instance/qrcode_generator.db`
- **Root directory:** `qrcode_generator.db`
- **Custom location:** As specified in your `.env` file via `DATABASE_URL`

The migration script automatically checks all common locations.

## Troubleshooting

### Migration fails with "no such table: qr_codes"

**Cause:** Your database file exists but is empty or corrupted.

**Solution:**
1. Delete the database file:
   ```bash
   rm instance/qrcode_generator.db  # Linux/Mac
   del instance\qrcode_generator.db  # Windows
   ```
2. Run the application to create a fresh database:
   ```bash
   python app.py
   ```

### Migration fails with "database is locked"

**Cause:** The application is still running and has the database locked.

**Solution:**
1. Stop the application (press Ctrl+C if running in terminal)
2. Wait a few seconds
3. Run the migration script again

### Custom database location

**If you're using a custom database location** (via `DATABASE_URL` environment variable):

1. The migration script reads from your configuration
2. Make sure your `.env` file is properly configured
3. The migration script supports any database backend (SQLite, PostgreSQL, MySQL, etc.)

## Need More Help?

- Check the main [README.md](README.md) for general setup instructions
- Review the [SETUP.md](SETUP.md) for detailed installation steps
- Report issues on the GitHub repository

## Prevention

To avoid schema issues in the future:

1. **Always backup your database** before upgrading the application
2. **Read the release notes** when updating to see if migrations are needed
3. **Use version control** for your database if in production
4. **Consider using Flask-Migrate** for more complex schema changes in the future

---

**Last Updated:** 2026-02-10
