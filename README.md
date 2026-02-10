# IBQ QR Code Generator

![QR Code Generator](https://img.shields.io/badge/QR-Code-Generator-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-red)

Professional QR code generator specifically designed for business/visiting cards with unlimited generation capability.

## Features

### 🎯 Core Features
- **Unlimited QR Code Generation** - No throttling or rate limits
- **Multiple Output Formats** - PNG, SVG, and PDF support
- **vCard Format** - Standard business card contact format
- **Customization Options** - Size, colors, error correction, borders
- **Logo Integration** - Add custom logos to QR codes
- **Batch Processing** - Generate multiple QR codes at once

### 🌐 Web Interface
- Clean, intuitive user interface
- Real-time form validation
- Instant preview
- One-click download
- Responsive design

### 🚀 RESTful API
- FastAPI-powered endpoints
- Comprehensive API documentation
- JSON input/output
- Error handling and validation
- Batch generation support

### ⚡ Performance
- Efficient QR code generation
- Built-in caching mechanism
- Optimized for high-volume usage
- Asynchronous processing support

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/MUSTAQ-AHAMMAD/IBQ-QR-Code-Generator.git
cd IBQ-QR-Code-Generator
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment (optional)**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the application**
```bash
python -m uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

## Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Fill in the business card information
3. Customize QR code settings (optional)
4. Click "Generate QR Code"
5. Download your QR code

### API Endpoints

#### Generate Single QR Code
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "business_card": {
      "name": "John Doe",
      "phone": "+1-234-567-8900",
      "email": "john.doe@company.com",
      "company": "Tech Corp",
      "job_title": "Software Engineer",
      "website": "https://www.company.com"
    },
    "size": 10,
    "border": 4,
    "error_correction": "H",
    "foreground_color": "black",
    "background_color": "white",
    "output_format": "png",
    "include_logo": false
  }'
```

#### Batch Generate QR Codes
```bash
curl -X POST "http://localhost:8000/api/v1/batch-generate" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "business_card": {"name": "User 1", "email": "user1@example.com"},
      "output_format": "png"
    },
    {
      "business_card": {"name": "User 2", "email": "user2@example.com"},
      "output_format": "svg"
    }
  ]'
```

#### Download QR Code
```bash
curl -O "http://localhost:8000/api/v1/download/{filename}"
```

### Python API

```python
from app.models.business_card import BusinessCard, QRCodeRequest
from app.core.qr_generator import QRCodeGenerator

# Create business card
card = BusinessCard(
    name="John Doe",
    phone="+1-234-567-8900",
    email="john.doe@company.com",
    company="Tech Corp",
    job_title="Software Engineer"
)

# Create QR code request
request = QRCodeRequest(
    business_card=card,
    size=10,
    border=4,
    error_correction="H",
    output_format="png"
)

# Generate QR code
generator = QRCodeGenerator()
filename, file_path = generator.generate(request)
print(f"QR code saved to: {file_path}")
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Application Settings
APP_NAME=IBQ QR Code Generator
DEBUG=True

# QR Code Settings
DEFAULT_QR_SIZE=10
DEFAULT_BORDER=4
DEFAULT_ERROR_CORRECTION=H
OUTPUT_DIRECTORY=output

# Cache Settings
ENABLE_CACHE=True
CACHE_EXPIRY_SECONDS=3600
```

### QR Code Options

- **Size**: 1-50 (box size in pixels)
- **Border**: 0-10 (border width in boxes)
- **Error Correction**:
  - L: 7% error recovery
  - M: 15% error recovery
  - Q: 25% error recovery
  - H: 30% error recovery (recommended)
- **Output Formats**: PNG, SVG, PDF
- **Colors**: Any valid color name or hex code

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_vcard.py
```

## Project Structure

```
IBQ-QR-Code-Generator/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── qr_routes.py     # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── qr_generator.py  # Core QR generation
│   │   └── vcard.py         # vCard formatter
│   └── models/
│       ├── __init__.py
│       └── business_card.py # Data models
├── templates/
│   └── index.html           # Web interface
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── tests/
│   ├── __init__.py
│   ├── test_vcard.py
│   ├── test_qr_generator.py
│   └── test_api.py
├── output/                  # Generated QR codes
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Security Considerations

- Input validation on all endpoints
- File size limits for logo uploads
- Sanitized file paths
- CORS configuration
- No sensitive data storage by default

## Performance Tips

1. **Enable Caching**: Set `ENABLE_CACHE=True` in `.env`
2. **Batch Processing**: Use batch endpoint for multiple QR codes
3. **Output Format**: SVG is smallest, PNG is most compatible
4. **Error Correction**: Higher levels increase QR code size

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- QR code generation by [qrcode](https://github.com/lincolnloop/python-qrcode)
- Styling inspired by modern web design principles

---

Made with ❤️ for business professionals worldwide