#!/bin/bash
#
# Database restore script for IBQ QR Code Generator
# Usage: ./restore_db.sh <backup_file>
#

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file>"
    echo "Example: $0 backups/qrcode_db_backup_20260516_120000.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "WARNING: This will restore the database from backup."
echo "Backup file: $BACKUP_FILE"
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

# Decompress if needed
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "Decompressing backup..."
    TEMP_FILE="${BACKUP_FILE%.gz}"
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    BACKUP_FILE="$TEMP_FILE"
    CLEANUP_TEMP=true
fi

echo "Starting database restore..."

# Check if running in Docker
if [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup 2>/dev/null; then
    echo "Running in Docker environment"
    psql -U "${POSTGRES_USER:-qrcode_user}" "${POSTGRES_DB:-qrcode_db}" < "$BACKUP_FILE"
else
    echo "Running in host environment"
    if command -v docker-compose &> /dev/null; then
        docker-compose exec -T db psql -U qrcode_user qrcode_db < "$BACKUP_FILE"
    else
        PGPASSWORD="${DB_PASSWORD}" psql -h localhost -U qrcode_user qrcode_db < "$BACKUP_FILE"
    fi
fi

# Cleanup temporary file
if [ "$CLEANUP_TEMP" = true ]; then
    rm -f "$TEMP_FILE"
fi

echo "Database restore completed successfully"
