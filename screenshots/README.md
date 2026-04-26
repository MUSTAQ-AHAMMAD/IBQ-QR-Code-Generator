# IBQ QR Code Generator - Application Screenshots

This directory contains screenshots of all the functionalities of the IBQ QR Code Generator application, demonstrating how each feature looks and works.

## 📸 Screenshot Overview

**Total Screenshots**: 31 captured screenshots organized into 7 categories

**Capture Date**: 2026-04-26

**Resolution**: 1920x1080 (Full HD)

---

## 📁 Directory Structure

```
screenshots/
├── 01-authentication/        # Login, registration, and public pages
├── 02-dashboard/             # Dashboard home with light/dark themes
├── 03-qr-generation/         # QR code generation for all 16 types
├── 04-qr-management/         # QR code management features
├── 05-templates/             # Template management
├── 06-settings/              # User settings and configuration
└── 07-help/                  # Help, documentation, and support
```

---

## 🔐 1. Authentication & Public Pages

### Location: `01-authentication/`

| Screenshot | Description | Features Shown |
|------------|-------------|----------------|
| `01-login-page.png` | User login page | Username/email field, password field, remember me checkbox, login button, link to registration |
| `02-registration-page.png` | User registration page | Username, email, first name, last name, password fields, terms acceptance, registration form |

**Key Features**:
- Clean and modern authentication interface
- Built-in form validation
- Secure password handling
- Direct links between login and registration

---

## 🏠 2. Dashboard & Home

### Location: `02-dashboard/`

| Screenshot | Description | Features Shown |
|------------|-------------|----------------|
| `01-dashboard-home-light.png` | Dashboard home page (Light theme) | Statistics cards, recent activity, quick actions, navigation sidebar, user menu |
| `02-dashboard-home-dark.png` | Dashboard home page (Dark theme) | Same features in dark mode, theme toggle button, persistent theme preference |

**Key Features**:
- Real-time statistics (total QR codes, this month, this week)
- Activity timeline
- Quick navigation sidebar
- Light/Dark theme toggle
- Responsive layout
- User profile access

---

## 🎨 3. QR Code Generation (All 16 Types)

### Location: `03-qr-generation/`

The application supports 16 different QR code types, each with specialized form fields:

| Screenshot | QR Code Type | Use Case | Key Fields |
|------------|--------------|----------|------------|
| `01-generate-business-card.png` | **Business Card / vCard** | Digital contact information | Name, title, email, phone, company, website, address |
| `02-generate-url.png` | **Website URL** | Direct link to websites | URL field |
| `03-generate-text.png` | **Plain Text** | Any text content | Text content area |
| `04-generate-email.png` | **Email** | Pre-filled email message | Email address, subject, body |
| `05-generate-sms.png` | **SMS / Text Message** | Text messages with content | Phone number, message |
| `06-generate-phone.png` | **Phone Number** | One-tap calling | Phone number field |
| `07-generate-wifi.png` | **WiFi Network** | Network connection sharing | SSID, password, security type, hidden network option |
| `08-generate-facebook.png` | **Facebook Profile** | Social media linking | Profile URL |
| `09-generate-twitter.png` | **Twitter Profile** | Social media linking | Profile URL |
| `10-generate-instagram.png` | **Instagram Profile** | Social media linking | Profile URL |
| `11-generate-linkedin.png` | **LinkedIn Profile** | Professional networking | Profile URL |
| `12-generate-youtube.png` | **YouTube Channel** | Video channel linking | Channel URL |
| `13-generate-appstore.png` | **App Store Link** | Apple app downloads | App Store URL |
| `14-generate-playstore.png` | **Google Play Store** | Android app downloads | Google Play URL |
| `15-generate-calendar.png` | **Calendar Event** | Event invitations | Title, location, start/end time, description |
| `16-generate-location.png` | **Location / Map** | Geographic coordinates | Latitude, longitude, location name |

**Common Features Across All Types**:
- QR code name and description fields
- Category selection (Business, Personal, Event, Product, Other)
- Dynamic form fields that change based on QR type selection
- Customization options (colors, size, error correction)
- Format selection (PNG, SVG, PDF)
- Template application
- Contextual help tips in sidebar
- Real-time form validation

---

## 📋 4. QR Code Management

### Location: `04-qr-management/`

| Screenshot | Description | Features Shown |
|------------|-------------|----------------|
| `01-my-qrcodes-list.png` | List of all generated QR codes | QR code thumbnails, names, types, creation dates, search/filter, action buttons (view, edit, download, delete) |

**Key Features**:
- Grid/List view of QR codes
- Search functionality
- Filter by category and type
- QR code preview thumbnails
- Quick actions for each QR code
- Pagination for large collections
- View count and download statistics

**Note**: Screenshots for individual QR code view and edit pages would show after generating sample codes. The captured screenshot shows the list view with the three sample QR codes that were generated (GitHub Repository URL, Welcome Message text, and Contact Support email).

---

## 🎨 5. Template Management

### Location: `05-templates/`

| Screenshot | Description | Features Shown |
|------------|-------------|----------------|
| `01-templates-list.png` | Available templates | Default templates (Professional Black, Modern Blue, Elegant Purple), template cards with previews, create new template button |
| `02-create-template.png` | Template creation form | Template name, description, category, foreground/background color pickers, public/private toggle |

**Key Features**:
- Pre-built default templates
- Custom template creation
- Color customization with visual pickers
- Template categories
- Public/private template options
- Template preview
- Easy template application to new QR codes

---

## ⚙️ 6. Settings Pages

### Location: `06-settings/`

| Screenshot | Description | Features Shown |
|------------|-------------|----------------|
| `01-profile-settings.png` | User profile settings | First name, last name, email, username, photo upload, profile information update |
| `02-change-password.png` | Password change form | Current password, new password, confirm password fields, password strength indicator |
| `03-account-settings.png` | Account settings | Account status, email notifications, privacy settings, account management options |
| `04-api-key.png` | API key management | API key generation, regeneration, copy functionality, API documentation link |

**Key Features**:
- Comprehensive user profile management
- Secure password change workflow
- Account security settings
- API key generation for programmatic access
- Email notification preferences
- Privacy controls

---

## 📚 7. Help & Support Pages

### Location: `07-help/`

| Screenshot | Description | Features Shown |
|------------|-------------|----------------|
| `01-documentation.png` | Complete documentation | User guides, feature documentation, getting started guide, technical details |
| `02-faq.png` | Frequently Asked Questions | Common questions and answers organized by category, expandable sections |
| `03-contact.png` | Contact support form | Name, email, subject, message fields, contact form submission |
| `04-help.png` | Help center home | Help topics, search functionality, popular articles, support resources |

**Key Features**:
- Comprehensive documentation
- Searchable FAQ
- Direct contact form
- Multiple support channels
- Context-sensitive help
- Tutorial resources

---

## 🎯 Application Highlights

### Design & UI
- **Modern Bootstrap 5 Interface**: Professional, responsive design
- **Dark/Light Theme**: User-selectable with persistence
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Intuitive Navigation**: Clear sidebar menu with organized sections
- **Visual Feedback**: Real-time validation and user notifications

### Functionality
- **16 QR Code Types**: Comprehensive coverage of use cases
- **Unlimited Generation**: No throttling or limits
- **Multiple Formats**: PNG, SVG, PDF export options
- **Template System**: Save and reuse favorite settings
- **Search & Filter**: Easy QR code organization and retrieval
- **Statistics Tracking**: View and download counts

### Security
- **User Authentication**: Secure login system
- **Password Hashing**: Bcrypt protection
- **Session Management**: Secure session handling
- **CSRF Protection**: Form security
- **Account Lockout**: Failed login attempt protection
- **API Key Management**: Secure programmatic access

---

## 📖 Usage Notes

### Viewing Screenshots
- All screenshots are in PNG format at 1920x1080 resolution
- Images capture full-page views where appropriate
- Both light and dark theme variants are included for the dashboard

### Screenshot Capture Method
- Automated capture using Playwright browser automation
- Chromium browser in headless mode
- Authenticated session to capture protected pages
- Full-page screenshots for comprehensive view

### File Naming Convention
- Format: `##-descriptive-name.png`
- Numbered sequentially within each category
- Descriptive names for easy identification

---

## 🚀 Getting Started

To explore these features in the live application:

1. **Install the application**:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

2. **Access the application**:
   - Navigate to: http://localhost:5000
   - Default credentials:
     - Username: `admin`
     - Password: `admin123`

3. **Explore features**:
   - Start with the dashboard to see statistics
   - Try generating QR codes of different types
   - Create custom templates
   - Manage your QR code collection

---

## 📄 Additional Resources

- **Main README**: `../README.md` - Complete application documentation
- **API Documentation**: `../API_DOCUMENTATION.md` - API endpoints and usage
- **Setup Guide**: `../SETUP.md` - Detailed installation instructions
- **QR Types Guide**: `../QR_CODE_TYPES_GUIDE.md` - Detailed guide for all QR types
- **Deployment Guide**: `../DEPLOYMENT.md` - Production deployment instructions

---

## 🤝 Contributing

If you'd like to contribute additional screenshots or update existing ones:

1. Run the screenshot capture script:
   ```bash
   python capture_screenshots.py
   ```

2. New screenshots will be saved in the appropriate category folders

3. Update this README if adding new categories or features

---

## 📝 License

These screenshots are part of the IBQ QR Code Generator project and follow the same MIT License as the main application.

---

**Made with ❤️ by MUSTAQ-AHAMMAD**

*Last Updated: 2026-04-26*
