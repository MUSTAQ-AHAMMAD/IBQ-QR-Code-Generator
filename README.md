# IBQ QR Code Generator

A comprehensive, production-ready Python web application for generating QR codes with support for 16 different types. Built with Flask and featuring a complete authentication system, professional dashboard, and unlimited QR code generation capabilities.

## Features

### Authentication & Security
- **User Authentication**: Complete login/registration system
- **Password Security**: Bcrypt password hashing
- **Session Management**: Secure session handling with timeout
- **CSRF Protection**: Built-in protection against cross-site request forgery
- **Account Security**: Failed login attempt tracking and account lockout

### Dashboard & Navigation
- **Professional Dashboard**: Modern, responsive interface with Bootstrap 5
- **Multi-level Navigation**: Organized sidebar menu with all features
- **Dark/Light Theme**: Toggle between themes with preference persistence
- **Quick Statistics**: Real-time stats on QR codes generated
- **Activity Timeline**: Track recent user actions

### QR Code Features
- **16 QR Code Types Supported**:
  - **Business Card / vCard**: Digital contact information in vCard format
  - **Website URL**: Direct links to any website
  - **Plain Text**: Encode any text information
  - **Email**: Pre-filled email with subject and body
  - **SMS**: Text messages with pre-filled content
  - **Phone**: Direct phone call initiation
  - **WiFi**: One-tap WiFi network connection
  - **Social Media**: Facebook, Twitter, Instagram, LinkedIn, YouTube profiles
  - **App Stores**: Apple App Store and Google Play Store links
  - **Calendar Events**: iCal format event details
  - **Location**: Geographic coordinates for maps
- **Unlimited Generation**: Create unlimited QR codes without throttling
- **Smart Form Interface**: Dynamic form fields based on selected QR code type
- **Customization**: Custom colors, sizes, error correction levels
- **Multiple Formats**: Export as PNG, SVG, or PDF
- **Template System**: Save and reuse favorite settings
- **QR Code Management**: View, edit, download, and delete QR codes

### Additional Features
- **Template Management**: Create custom templates or use pre-built ones
- **Search & Filter**: Easily find QR codes by name, description, or category
- **Download Tracking**: Monitor QR code views and downloads
- **API Key Generation**: For programmatic access (developer feature)
- **Comprehensive Help**: Documentation, FAQ, and support pages
- **Type-Specific Tips**: Contextual help for each QR code type

## Tech Stack

- **Backend**: Python 3.x with Flask 3.0
- **Database**: SQLAlchemy with SQLite (upgradeable to PostgreSQL)
- **Authentication**: Flask-Login for session management
- **Forms**: Flask-WTF with validation
- **QR Code**: qrcode library with PIL/Pillow
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Security**: Werkzeug password hashing, CSRF protection

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/MUSTAQ-AHAMMAD/IBQ-QR-Code-Generator.git
   cd IBQ-QR-Code-Generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and set your configuration
   # Important: Change the SECRET_KEY in production!
   ```

5. **Initialize the database**
   ```bash
   python app.py
   ```
   The database will be created automatically on first run.

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - Default admin credentials:
     - Username: `admin`
     - Password: `admin123`
   - **Important**: Change the admin password immediately after first login!

## Project Structure

```
IBQ-QR-Code-Generator/
├── app.py                  # Main application file
├── config.py              # Configuration management
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── utils.py               # QR code utilities
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard_base.html
│   ├── auth/            # Authentication pages
│   ├── dashboard/       # Dashboard pages
│   └── errors/          # Error pages
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── uploads/             # Generated QR codes (created automatically)
```

## Usage

### Generating Your First QR Code

1. Log in to your account
2. Click "Generate QR Code" in the sidebar
3. Select the QR Code Type from the dropdown:
   - **Business Card / vCard**: For contact information
   - **Website URL**: For directing to websites
   - **Plain Text**: For any text content
   - **Email**: For pre-filled emails
   - **SMS**: For text messages
   - **Phone**: For phone calls
   - **WiFi**: For WiFi network access
   - **Social Media**: For social profiles
   - **App Store**: For app downloads
   - **Calendar Event**: For event invitations
   - **Location**: For map directions
4. Fill in the relevant information for your selected type:
   - Form fields automatically update based on QR code type
   - Contextual tips appear in the sidebar
5. Customize appearance (optional):
   - Choose foreground and background colors
   - Set size and error correction level
   - Select output format (PNG, SVG, or PDF)
   - Apply a template
6. Click "Generate QR Code"
7. Download your QR code

### QR Code Type Examples

**Business Card**:
- Perfect for networking events and professional contacts
- Saves contact information directly to phone

**Website URL**:
- Direct customers to your website
- Link to product pages or promotions

**WiFi**:
- Share WiFi access with guests
- No need to manually enter passwords

**Email**:
- Pre-fill support emails
- Collect feedback easily

**SMS**:
- Quick customer service responses
- Contest entries and voting

**Phone**:
- One-tap calling for customer support
- Emergency contact information

For detailed examples and best practices, see [QR_CODE_TYPES_GUIDE.md](QR_CODE_TYPES_GUIDE.md)

### Managing QR Codes

- **View All**: Navigate to "My QR Codes" to see all generated codes
- **Search**: Use the search bar to find specific QR codes
- **Filter**: Filter by category or type
- **Edit**: Update name, description, and category
- **Download**: Download in the original format
- **Share**: Get shareable links for vCard types
- **Delete**: Remove unwanted QR codes

### Using Templates

1. Navigate to "Templates"
2. Click "Create Template"
3. Set your preferred colors and settings
4. Save the template
5. When generating new QR codes, select your template from the dropdown

## Configuration

### Environment Variables

Edit the `.env` file to configure:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///qrcode_generator.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=3600
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_DURATION=900
```

### Database Configuration

By default, the application uses SQLite. To use PostgreSQL:

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `DATABASE_URL` in `.env`:
   ```env
   DATABASE_URL=postgresql://username:password@localhost/dbname
   ```

## Security Features

- **Password Hashing**: All passwords are hashed using Werkzeug's security utilities
- **CSRF Protection**: All forms include CSRF tokens
- **Session Security**: Secure session cookies with configurable timeout
- **Account Lockout**: Automatic lockout after failed login attempts
- **Input Validation**: Server-side validation for all user inputs
- **SQL Injection Prevention**: SQLAlchemy ORM protects against SQL injection

## API Access

The application includes API key generation for programmatic access:

1. Navigate to Settings > API Key
2. Click "Generate API Key"
3. Copy and securely store your API key
4. Use the API key in your HTTP requests

## Troubleshooting

### Common Issues

**Database errors on startup**
- Delete the existing database file and restart the application
- Check file permissions in the project directory

**QR codes not displaying**
- Ensure the `uploads` folder exists and is writable
- Check file permissions

**Theme not persisting**
- Clear browser local storage
- Check browser console for JavaScript errors

**Upload errors**
- Check `MAX_CONTENT_LENGTH` in configuration
- Ensure sufficient disk space

## Development

### Running in Development Mode

```bash
# Set Flask environment
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows

# Run the application
python app.py
```

### Database Migrations

The application uses Flask-Migrate for database migrations:

```bash
# Initialize migrations (first time only)
flask db init

# Create a migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

## Production Deployment

### Preparation

1. **Update configuration**:
   - Set `FLASK_ENV=production`
   - Set `SECRET_KEY` to a strong random value
   - Set `SESSION_COOKIE_SECURE=True`
   - Configure production database

2. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Set up reverse proxy** (nginx example):
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

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

- **Documentation**: Available in the application under Help > Documentation
- **FAQ**: Check Help > FAQ for common questions
- **Issues**: Report bugs on GitHub Issues
- **Contact**: Use the contact form in the application

## Acknowledgments

- Flask framework and extensions
- Bootstrap 5 for UI components
- qrcode library for QR code generation
- Bootstrap Icons for icons

## Version History

### v2.0.0 (2026)
- **Major Feature Update**: Added support for 16 different QR code types
- New QR code types: URL, Text, Email, SMS, Phone, WiFi, Social Media, App Stores, Calendar Events, Location
- Dynamic form interface with type-specific fields
- Contextual help and tips for each QR code type
- Enhanced utils with specialized data generation functions
- Comprehensive QR Code Types Guide documentation
- Improved user experience with smart field visibility

### v1.0.0 (2024)
- Initial release
- Complete authentication system
- QR code generation and management (vCard/Business Card only)
- Template system
- Dark/light theme support
- Comprehensive documentation

---

**Made with ❤️ by MUSTAQ-AHAMMAD**
