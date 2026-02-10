# Deployment Guide

## Overview

This guide covers deploying the IBQ QR Code Generator to various environments.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Considerations](#production-considerations)

## Local Development

### Quick Start

1. **Clone and Setup**
```bash
git clone https://github.com/MUSTAQ-AHAMMAD/IBQ-QR-Code-Generator.git
cd IBQ-QR-Code-Generator
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run Application**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access Application**
- Web Interface: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create output directory
RUN mkdir -p output

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  qr-generator:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - OUTPUT_DIRECTORY=output
    volumes:
      - ./output:/app/output
    restart: unless-stopped
```

### Build and Run

```bash
docker-compose up -d
```

## Cloud Deployment

### Deploy to Heroku

1. **Create Procfile**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. **Deploy**
```bash
heroku create ibq-qr-generator
git push heroku main
```

### Deploy to Railway

1. **Connect Repository**
   - Go to https://railway.app
   - Connect your GitHub repository

2. **Configure**
   - Add start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Set environment variables

### Deploy to Google Cloud Run

1. **Create Dockerfile** (see Docker section)

2. **Deploy**
```bash
gcloud run deploy qr-generator \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Deploy to AWS (Elastic Beanstalk)

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize and Deploy**
```bash
eb init -p python-3.11 qr-generator
eb create qr-generator-env
eb open
```

### Deploy to Azure App Service

```bash
az webapp up --name ibq-qr-generator --runtime "PYTHON:3.11"
```

## Production Considerations

### 1. Security

**Environment Variables**
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com
```

**HTTPS/SSL**
- Always use HTTPS in production
- Use reverse proxy (Nginx, Apache)
- Enable SSL certificates (Let's Encrypt)

**Rate Limiting**
Add rate limiting to prevent abuse:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/generate")
@limiter.limit("10/minute")
async def generate_qr_code(request: Request, qr_request: QRCodeRequest):
    ...
```

### 2. Performance

**Caching**
- Enable Redis for distributed caching
- Set appropriate cache expiry times

**File Storage**
- Use cloud storage (S3, Google Cloud Storage) for generated QR codes
- Implement automatic cleanup of old files

**Load Balancing**
- Use multiple instances behind a load balancer
- Consider using Kubernetes for orchestration

### 3. Monitoring

**Logging**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Health Checks**
- Use `/api/v1/health` endpoint for health checks
- Set up uptime monitoring (UptimeRobot, Pingdom)

**Application Monitoring**
- Sentry for error tracking
- New Relic or DataDog for performance monitoring

### 4. Backup and Recovery

**Database Backups**
If using database for metadata:
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
sqlite3 qr_codes.db ".backup backup_$DATE.db"
```

**File Backups**
- Regular backups of generated QR codes
- Store backups in separate location

### 5. Scaling

**Horizontal Scaling**
- Multiple application instances
- Shared file storage (S3, NFS)
- Redis for shared cache

**Vertical Scaling**
- Increase CPU/RAM for single instance
- Monitor resource usage

### 6. Maintenance

**Updates**
```bash
# Update dependencies
pip install -U -r requirements.txt

# Run tests
pytest

# Deploy with zero downtime
```

**Cleanup**
```python
# Automated cleanup script
import os
import time
from pathlib import Path

def cleanup_old_files(directory, max_age_days=7):
    """Remove files older than max_age_days"""
    now = time.time()
    max_age = max_age_days * 86400
    
    for file in Path(directory).glob("*"):
        if file.is_file():
            age = now - file.stat().st_mtime
            if age > max_age:
                file.unlink()
```

## Nginx Configuration

**Example nginx.conf**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # SSL configuration
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

## Systemd Service

**Create /etc/systemd/system/qr-generator.service**
```ini
[Unit]
Description=IBQ QR Code Generator
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/qr-generator
Environment="PATH=/var/www/qr-generator/venv/bin"
ExecStart=/var/www/qr-generator/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start**
```bash
sudo systemctl enable qr-generator
sudo systemctl start qr-generator
sudo systemctl status qr-generator
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Enable debug mode | True |
| HOST | Server host | 0.0.0.0 |
| PORT | Server port | 8000 |
| DEFAULT_QR_SIZE | Default QR code size | 10 |
| DEFAULT_BORDER | Default border size | 4 |
| OUTPUT_DIRECTORY | Output directory for QR codes | output |
| ENABLE_CACHE | Enable caching | True |
| CACHE_EXPIRY_SECONDS | Cache expiry time | 3600 |

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Permission Issues
```bash
# Fix output directory permissions
chmod 755 output
chown -R www-data:www-data output
```

### Import Errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

## Support

For issues or questions:
- Open an issue on GitHub
- Check documentation at `/api/docs`
- Review logs for error messages

---

**Note**: Always test deployments in a staging environment before production.
