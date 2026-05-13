# Obsolete Migration Files

## Why These Files Are Marked as Obsolete

The following migration files have been marked as obsolete (with `.obsolete` extension):

1. `add_user_photo_profile_color.py.obsolete` (revision: a3b4c5d6e7f8)
2. `add_brands_table_and_brand_id.py.obsolete` (revision: b5c6d7e8f9g0)

## Reason

These migrations were originally created to incrementally add features to the database schema:
- `add_user_photo_profile_color.py` added user_photo and profile_color columns to the users table
- `add_brands_table_and_brand_id.py` added the brands table and brand_id foreign key to qr_codes

However, this created a problem:
- New installations using `db.create_all()` would have all columns (because models.py defines them)
- Installations using migrations would need to run multiple migration files to get the same schema
- This mismatch caused the "no such column: qr_codes.brand_id" error for users who had older databases

## Solution

All changes from these migrations have been consolidated into the initial migration file:
- `29c2fde25c94_initial_migration_create_all_tables.py` now includes:
  - brands table
  - brand_id column in qr_codes
  - company_logo, user_photo, and profile_color columns in users

This ensures that:
1. New installations get the complete schema from the start
2. There's only one migration to run (the initial one)
3. No schema mismatch between db.create_all() and migrations

## For Developers

If you're working on this codebase:

1. **Do not** restore these obsolete files - they will cause migration conflicts
2. **Do not** reference the revision IDs from these files (a3b4c5d6e7f8, b5c6d7e8f9g0)
3. **Do** start fresh with the updated initial migration
4. **Do** create new migrations for any future schema changes

## Migration Best Practices

Going forward:

1. Always create migrations for schema changes:
   ```bash
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```

2. Don't modify existing migrations that have been deployed
3. Keep migrations in sync with models.py
4. Test migrations on a copy of production data before deploying

## For Users Experiencing Issues

If you're experiencing database errors, see the comprehensive fix guide in:
`DATABASE_MIGRATION_FIX.md`

The recommended fix is to delete your database and let it be recreated with the correct schema (Option 1 in the fix guide).
