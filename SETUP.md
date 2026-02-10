# IBQ QR Code Generator - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and update SECRET_KEY for production
```

### 3. Initialize the Database

```bash
python init_db.py
```

This creates all database tables and sets up the default admin user and templates.

**Optional:** Seed sample data for development:
```bash
python seed_db.py
```

### 4. Run the Application

```bash
python app.py
```

The application will be available at: http://localhost:5000

### 5. Default Login

- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change the default password immediately!

## Features Overview

### Authentication System
- ✅ Secure login with session management
- ✅ User registration with validation
- ✅ Password hashing with bcrypt
- ✅ CSRF protection
- ✅ Account lockout after failed attempts
- ✅ Remember me functionality

### Dashboard
- ✅ Statistics dashboard (total, monthly, weekly QR codes)
- ✅ Quick action buttons
- ✅ Recent activity timeline
- ✅ Dark/light theme toggle
- ✅ Responsive design

### QR Code Generation
- ✅ Business card vCard format
- ✅ Customizable colors and sizes
- ✅ Multiple output formats (PNG, SVG, PDF)
- ✅ Error correction levels
- ✅ Template support
- ✅ Unlimited generation

### Management
- ✅ View all QR codes in grid layout
- ✅ Search and filter functionality
- ✅ Edit QR code metadata
- ✅ Download QR codes
- ✅ Delete with confirmation
- ✅ Track downloads and views

### Templates
- ✅ Create custom templates
- ✅ Pre-built default templates
- ✅ Public/private templates
- ✅ Usage tracking

### Settings
- ✅ User profile management
- ✅ Account preferences
- ✅ Password change
- ✅ API key generation

### Help & Support
- ✅ Comprehensive documentation
- ✅ FAQ section
- ✅ Help guides
- ✅ Contact form

## Project Structure

```
IBQ-QR-Code-Generator/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── forms.py              # WTForms definitions
├── utils.py              # QR code utilities
├── init_db.py            # Database initialization script
├── seed_db.py            # Database seeding script (sample data)
├── migrate_db.py         # Database migration script
├── migrations/           # Flask-Migrate migrations
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── templates/           # Jinja2 templates
│   ├── auth/           # Authentication pages
│   ├── dashboard/      # Dashboard pages
│   └── errors/         # Error pages
├── static/             # Static assets
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
└── uploads/           # Generated QR codes
```

## Database Models

### User
- Authentication and user management
- Password hashing and security
- API key generation
- Theme preferences

### QRCode
- Generated QR code storage
- Business card information
- Customization settings
- Download/view statistics

### Template
- Reusable QR code settings
- Public/private templates
- Usage tracking

### AuditLog
- User activity tracking
- Security monitoring
- Action logging

## Security Features

1. **Password Security**
   - Bcrypt hashing
   - Minimum length requirements
   - Strength validation

2. **Session Security**
   - Secure session cookies
   - Configurable timeout
   - HTTP-only cookies

3. **CSRF Protection**
   - All forms protected
   - Token validation

4. **Account Security**
   - Failed login tracking
   - Account lockout
   - IP logging

## Configuration

Edit `.env` file for customization:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///qrcode_generator.db
UPLOAD_FOLDER=uploads
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_DURATION=900
SESSION_COOKIE_SECURE=False  # Set to True in production with HTTPS
```

## Upgrading to PostgreSQL

1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

2. Update DATABASE_URL in .env:
```env
DATABASE_URL=postgresql://username:password@localhost/dbname
```

## Production Deployment

1. **Update Configuration**
   - Set `FLASK_ENV=production`
   - Generate strong `SECRET_KEY`
   - Set `SESSION_COOKIE_SECURE=True`
   - Configure production database

2. **Use Production Server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. **Set Up Reverse Proxy** (nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/IBQ-QR-Code-Generator/static;
    }
}
```

4. **Enable HTTPS** with Let's Encrypt

## Troubleshooting

### Database Issues
- Run `python init_db.py` to initialize the database
- Run `python init_db.py --drop` to recreate the database from scratch
- Run `python migrate_db.py` if upgrading from an older version
- Use `flask db upgrade` to apply pending migrations
- Delete `qrcode_generator.db` and restart
- Check file permissions

### Upload Issues
- Ensure `uploads/` folder exists
- Check write permissions

### Theme Not Persisting
- Clear browser localStorage
- Check browser console for errors

## Support

For issues and questions:
- Check the FAQ in the application
- Read the documentation
- Open an issue on GitHub

## License

MIT License - see LICENSE file for details
