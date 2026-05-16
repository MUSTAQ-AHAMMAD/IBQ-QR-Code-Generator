#!/bin/bash
#
# Database backup script for IBQ QR Code Generator
# Usage: ./backup_db.sh [backup_directory]
#

set -e

# Configuration
BACKUP_DIR="${1:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="qrcode_db_backup_${TIMESTAMP}.sql"
RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "Starting database backup..."

# Check if running in Docker
if [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup 2>/dev/null; then
    echo "Running in Docker environment"
    # Backup from within container
    pg_dump -U "${POSTGRES_USER:-qrcode_user}" "${POSTGRES_DB:-qrcode_db}" > "${BACKUP_DIR}/${BACKUP_FILE}"
else
    echo "Running in host environment"
    # Backup using docker-compose
    if command -v docker-compose &> /dev/null; then
        docker-compose exec -T db pg_dump -U qrcode_user qrcode_db > "${BACKUP_DIR}/${BACKUP_FILE}"
    else
        # Direct PostgreSQL backup
        PGPASSWORD="${DB_PASSWORD}" pg_dump -h localhost -U qrcode_user qrcode_db > "${BACKUP_DIR}/${BACKUP_FILE}"
    fi
fi

# Compress backup
gzip "${BACKUP_DIR}/${BACKUP_FILE}"
BACKUP_FILE="${BACKUP_FILE}.gz"

echo "Backup created: ${BACKUP_DIR}/${BACKUP_FILE}"

# Get backup size
BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
echo "Backup size: ${BACKUP_SIZE}"

# Remove old backups
echo "Cleaning up old backups (older than ${RETENTION_DAYS} days)..."
find "$BACKUP_DIR" -name "qrcode_db_backup_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete

# Count remaining backups
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "qrcode_db_backup_*.sql.gz" -type f | wc -l)
echo "Total backups: ${BACKUP_COUNT}"

echo "Database backup completed successfully"

# Optional: Upload to S3 or remote storage
# aws s3 cp "${BACKUP_DIR}/${BACKUP_FILE}" s3://your-bucket/backups/
