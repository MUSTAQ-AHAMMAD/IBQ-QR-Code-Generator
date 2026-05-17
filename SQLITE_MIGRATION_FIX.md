# SQLite Migration Fix - organization_id Column Error

## Problem

When running the application with an existing SQLite database, you may encounter this error:

```
sqlite3.OperationalError: no such column: users.organization_id
```

This error occurs because:
1. The database was created with an older schema that didn't include the `organization_id` column
2. The migration code used PostgreSQL/MySQL syntax (`ADD COLUMN IF NOT EXISTS`) which is **not supported by SQLite**
3. When the app tries to query users at startup, SQLAlchemy attempts to select all columns including the missing `organization_id`

## Root Cause

SQLite does not support the `IF NOT EXISTS` clause with `ALTER TABLE ADD COLUMN`. The original migration code in `app.py` and `migrations_v2.py` used:

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS organization_id INTEGER
```

This syntax fails silently in SQLite, leaving the column unaddedd, which causes subsequent queries to fail.

## Solution

The fix checks for column existence using SQLAlchemy's inspector before attempting to add columns. This approach works across all database backends (SQLite, PostgreSQL, MySQL).

### Changes Made

1. **app.py** (lines 36-115): Updated `_run_database_migrations()` function
   - Added SQLAlchemy inspector to check if columns/indexes exist
   - Only executes `ALTER TABLE` if column doesn't exist
   - Removed `IF NOT EXISTS` from SQL statements

2. **migrations_v2.py** (lines 20-108): Updated migration logic
   - Same approach: check before adding columns/indexes
   - Better error messages showing what was added vs what already exists

### How It Works

```python
from sqlalchemy import inspect

inspector = inspect(db.engine)

def column_exists(table_name, column_name):
    if table_name not in inspector.get_table_names():
        return False
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

# Only add if missing
if not column_exists('users', 'organization_id'):
    conn.execute(text('ALTER TABLE users ADD COLUMN organization_id INTEGER'))
    conn.commit()
```

## How to Apply the Fix

If you have an existing database with this error:

1. **Update your code** by pulling the latest changes:
   ```bash
   git pull origin claude/fix-sqlite-no-such-column-error
   ```

2. **Restart the application**:
   ```bash
   python app.py
   ```

   The migration will run automatically on startup and add the missing columns.

3. **Verify the fix**:
   - The application should start without errors
   - You should see migration messages in the console
   - You can log in and access the dashboard

## Prevention

For future database schema changes:

1. **Never use `IF NOT EXISTS` with SQLite** - Always check column existence programmatically
2. **Test migrations with SQLite** before deploying
3. **Use the pattern from this fix** for all future migrations

## Technical Details

### Why SQLite Doesn't Support IF NOT EXISTS

SQLite has limited `ALTER TABLE` support compared to PostgreSQL/MySQL:
- ✅ Supported: `ALTER TABLE table ADD COLUMN column_name column_type`
- ❌ Not supported: `ALTER TABLE table ADD COLUMN IF NOT EXISTS ...`
- ❌ Not supported: `ALTER TABLE table DROP COLUMN ...`
- ❌ Not supported: `ALTER TABLE table MODIFY COLUMN ...`

### Database Compatibility

The fix ensures the application works correctly with:
- SQLite (local development, small deployments)
- PostgreSQL (recommended for production)
- MySQL/MariaDB (alternative for production)

## Testing

The fix was verified with a standalone test:
```bash
✓ Created test users table without organization_id
Before migration - organization_id exists: False
✓ Added organization_id column
After migration - columns: ['id', 'username', 'email', 'password_hash', 'organization_id']
After migration - organization_id exists: True
✓ Test passed - migration works correctly with SQLite
```

## Related Files

- `app.py`: Main application with startup migrations
- `migrations_v2.py`: Additional migration script
- `migrate_db.py`: Standalone migration tool (already uses correct approach)
- `models.py`: Database models with `organization_id` defined

## Support

If you encounter any issues:
1. Check that you're running the latest code
2. Try deleting the database and letting it recreate (only for development!)
3. Review the console output for migration warnings
4. Report issues with the full error message and steps to reproduce
