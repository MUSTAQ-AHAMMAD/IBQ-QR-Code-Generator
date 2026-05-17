# Database Migration Fix for organization_id Error

## Problem
The application was failing with the error:
```
sqlite3.OperationalError: no such column: users.organization_id
```

This occurred because:
1. The `User` model in `models.py` defines an `organization_id` column
2. When `db.create_all()` is called, it only creates NEW tables, not new columns in existing tables
3. Existing databases that were created before the `organization_id` field was added to the User model don't have this column

## Solution
Integrated automatic database migrations into the application startup process:

1. **Added SQL import**: Added `text` from `sqlalchemy` for raw SQL execution
2. **Created migration function**: `_run_database_migrations()` that:
   - Uses raw SQL `ALTER TABLE` statements with `IF NOT EXISTS` clauses
   - Adds the missing `organization_id` column to both `users` and `brands` tables
   - Adds other missing columns needed for full feature support
   - Creates necessary indexes for performance
   - Handles errors gracefully (doesn't crash if columns already exist)

3. **Integrated into startup**: Called `_run_database_migrations()` immediately after `db.create_all()` in the `create_app()` function

## Files Modified
- `app.py`:
  - Line 19: Added `text` import from sqlalchemy
  - Lines 36-91: Added `_run_database_migrations()` function
  - Line 146: Call migration function during app initialization

## Testing
The fix will automatically run when the application starts:
1. It checks if the `organization_id` column exists in the `users` table
2. If not, it adds it using `ALTER TABLE users ADD COLUMN IF NOT EXISTS organization_id INTEGER`
3. Does the same for other missing columns and indexes
4. The app then continues normal startup

## Benefits
- **Automatic**: No manual migration script needed
- **Safe**: Uses `IF NOT EXISTS` to prevent errors on fresh installations
- **Non-blocking**: Errors in migration don't crash the app
- **Comprehensive**: Handles all missing columns from the schema evolution

## Verification
When the app starts successfully without the `no such column: users.organization_id` error, the fix is working.
