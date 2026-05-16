#!/bin/bash
#
# Health check script for monitoring
# Returns 0 if healthy, 1 if unhealthy
#

set -e

# Configuration
APP_URL="${APP_URL:-http://localhost:8000}"
TIMEOUT=10

# Check health endpoint
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout $TIMEOUT "${APP_URL}/health" || echo "000")

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✓ Application is healthy (HTTP $HTTP_STATUS)"
    exit 0
else
    echo "✗ Application is unhealthy (HTTP $HTTP_STATUS)"
    exit 1
fi
