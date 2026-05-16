# Production Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the IBQ QR Code Generator to production environments.

## Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.11+, PostgreSQL 15+, Redis 7+, Nginx
- SSL certificates for HTTPS
- Domain name configured

## Quick Start with Docker

### 1. Clone and Configure

```bash
# Clone the repository
git clone https://github.com/MUSTAQ-AHAMMAD/IBQ-QR-Code-Generator.git
cd IBQ-QR-Code-Generator

# Create environment file
cp .env.example .env

# Edit .env with production values
nano .env
```

### 2. Required Environment Variables

```env
# Flask
FLASK_ENV=production
SECRET_KEY=<generate-strong-random-key>

# Database
DATABASE_URL=postgresql://qrcode_user:SECURE_PASSWORD@db:5432/qrcode_db
DB_PASSWORD=SECURE_PASSWORD

# Redis
REDIS_URL=redis://:SECURE_REDIS_PASSWORD@redis:6379/0
REDIS_PASSWORD=SECURE_REDIS_PASSWORD

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Strict

# Rate Limiting
RATELIMIT_ENABLED=True
RATELIMIT_DEFAULT=100 per hour
RATELIMIT_LOGIN=5 per minute

# Monitoring (optional)
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=production

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 3. Generate Secure Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Generate database password
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate Redis password
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. SSL Configuration

Place your SSL certificates in `nginx/ssl/`:

```bash
mkdir -p nginx/ssl
cp /path/to/your/cert.pem nginx/ssl/
cp /path/to/your/key.pem nginx/ssl/
```

Or use Let's Encrypt:

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Obtain certificate
certbot certonly --nginx -d your-domain.com -d www.your-domain.com

# Link certificates
ln -s /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
ln -s /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem
```

### 5. Update Nginx Configuration

Edit `nginx/nginx.conf`:

```nginx
# Change server_name
server_name your-domain.com www.your-domain.com;

# Uncomment HTTPS redirect in HTTP server block
return 301 https://$server_name$request_uri;
```

### 6. Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# Check logs
docker-compose logs -f web

# Check service status
docker-compose ps
```

### 7. Initialize Database

```bash
# Run migrations
docker-compose exec web flask db upgrade

# Create admin user (if needed)
docker-compose exec web python -c "
from app import create_app, db
from models import User

app = create_app('production')
with app.app_context():
    admin = User(
        username='admin',
        email='admin@yourdomain.com',
        first_name='Admin',
        last_name='User',
        is_verified=True,
        is_active=True
    )
    admin.set_password('CHANGE_THIS_PASSWORD')
    db.session.add(admin)
    db.session.commit()
    print('Admin user created')
"
```

### 8. Verify Deployment

```bash
# Test health endpoint
curl http://localhost/health

# Test HTTPS
curl https://your-domain.com/health

# Check application logs
docker-compose logs -f web

# Check nginx logs
docker-compose logs -f nginx
```

## Manual Deployment (Without Docker)

### 1. System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3-pip \
    postgresql-15 redis-server nginx supervisor

# Create application user
sudo useradd -m -s /bin/bash qrcode
sudo su - qrcode
```

### 2. Application Setup

```bash
# Clone repository
git clone https://github.com/MUSTAQ-AHAMMAD/IBQ-QR-Code-Generator.git
cd IBQ-QR-Code-Generator

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements-prod.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with production values
```

### 3. Database Setup

```bash
# Create PostgreSQL user and database
sudo -u postgres psql << EOF
CREATE USER qrcode_user WITH PASSWORD 'SECURE_PASSWORD';
CREATE DATABASE qrcode_db OWNER qrcode_user;
GRANT ALL PRIVILEGES ON DATABASE qrcode_db TO qrcode_user;
\q
EOF

# Run migrations
export FLASK_APP=wsgi.py
flask db upgrade
```

### 4. Gunicorn Configuration

Create `/home/qrcode/gunicorn_config.py`:

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 60
keepalive = 5

# Logging
accesslog = "/home/qrcode/IBQ-QR-Code-Generator/logs/gunicorn-access.log"
errorlog = "/home/qrcode/IBQ-QR-Code-Generator/logs/gunicorn-error.log"
loglevel = "info"

# Process naming
proc_name = "ibq-qr-generator"

# Server mechanics
daemon = False
pidfile = "/home/qrcode/IBQ-QR-Code-Generator/gunicorn.pid"
```

### 5. Supervisor Configuration

Create `/etc/supervisor/conf.d/qrcode.conf`:

```ini
[program:qrcode]
directory=/home/qrcode/IBQ-QR-Code-Generator
command=/home/qrcode/IBQ-QR-Code-Generator/venv/bin/gunicorn -c gunicorn_config.py wsgi:app
user=qrcode
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/qrcode/IBQ-QR-Code-Generator/logs/supervisor.log
environment=PATH="/home/qrcode/IBQ-QR-Code-Generator/venv/bin"
```

Start supervisor:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start qrcode
sudo supervisorctl status qrcode
```

### 6. Nginx Configuration

Create `/etc/nginx/sites-available/qrcode`:

```nginx
# Copy content from nginx/nginx.conf
# Adjust paths for manual deployment
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/qrcode /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Kubernetes Deployment

See `k8s/` directory for Kubernetes manifests (if you want to create them).

## Monitoring and Maintenance

### Health Checks

- Health: `https://your-domain.com/health`
- Readiness: `https://your-domain.com/ready`
- Metrics: `https://your-domain.com/metrics` (requires login)

### Log Management

```bash
# View application logs
docker-compose logs -f web

# View nginx logs
docker-compose logs -f nginx

# View database logs
docker-compose logs -f db
```

### Database Backups

```bash
# Backup database
docker-compose exec db pg_dump -U qrcode_user qrcode_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
docker-compose exec -T db psql -U qrcode_user qrcode_db < backup_file.sql

# Automated backups (add to crontab)
0 2 * * * cd /path/to/app && ./scripts/backup_db.sh
```

### Scaling

```bash
# Scale web service
docker-compose up -d --scale web=3

# Behind load balancer, update nginx upstream
```

## Security Checklist

- [ ] Changed default admin password
- [ ] Strong SECRET_KEY generated
- [ ] Database password is strong
- [ ] Redis password configured
- [ ] SSL certificates installed
- [ ] HTTPS redirect enabled
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Firewall configured (only 80, 443 open)
- [ ] Regular backups scheduled
- [ ] Monitoring configured
- [ ] Log rotation enabled

## Troubleshooting

### Application won't start

```bash
# Check logs
docker-compose logs web

# Check environment variables
docker-compose exec web env | grep FLASK

# Verify database connection
docker-compose exec web python -c "from app import create_app, db; app = create_app('production'); app.app_context().push(); db.session.execute('SELECT 1')"
```

### Database connection errors

```bash
# Check database is running
docker-compose ps db

# Check database credentials
docker-compose exec db psql -U qrcode_user -d qrcode_db

# Reset database password
docker-compose exec db psql -U postgres -c "ALTER USER qrcode_user PASSWORD 'new_password';"
```

### SSL certificate errors

```bash
# Check certificate validity
openssl x509 -in nginx/ssl/cert.pem -text -noout

# Renew Let's Encrypt
certbot renew --nginx
```

## Performance Optimization

### 1. Database Optimization

```sql
-- Add indexes (already in migrations)
CREATE INDEX idx_qrcodes_user_created ON qr_codes(user_id, created_at DESC);
CREATE INDEX idx_qrcodes_brand ON qr_codes(brand_id);
CREATE INDEX idx_audit_user_created ON audit_logs(user_id, created_at DESC);
```

### 2. Redis Caching

Enable Redis for sessions and caching (already configured in docker-compose).

### 3. CDN Integration

Upload static files and uploads to CDN:

```bash
# AWS S3 + CloudFront
aws s3 sync static/ s3://your-bucket/static/
aws s3 sync uploads/ s3://your-bucket/uploads/

# Update configuration to use CDN URLs
```

### 4. Image Optimization

QR codes are already optimized. For uploaded images:

```bash
# Install optimization tools
apt-get install optipng jpegoptim

# Optimize existing images
find uploads -name "*.png" -exec optipng {} \;
find uploads -name "*.jpg" -exec jpegoptim --strip-all {} \;
```

## Updates and Maintenance

### Updating the Application

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build

# Update dependencies
docker-compose exec web pip install -r requirements-prod.txt

# Run migrations
docker-compose exec web flask db upgrade

# Restart services
docker-compose restart web

# Zero-downtime update
docker-compose up -d --no-deps --build web
```

### Rollback

```bash
# Rollback code
git checkout previous-commit

# Rebuild and restart
docker-compose up -d --build

# Rollback database (if needed)
docker-compose exec web flask db downgrade
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/MUSTAQ-AHAMMAD/IBQ-QR-Code-Generator/issues
- Documentation: Check docs/ directory

## License

MIT License - see LICENSE file
