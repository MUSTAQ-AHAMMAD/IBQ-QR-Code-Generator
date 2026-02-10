# API Documentation

## Overview

The IBQ QR Code Generator provides a RESTful API for generating QR codes from business card information.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, no authentication is required. For production use, consider implementing API keys or OAuth2.

## Endpoints

### 1. Generate QR Code

Generate a single QR code from business card data.

**Endpoint:** `POST /generate`

**Request Body:**
```json
{
  "business_card": {
    "name": "John Doe",
    "phone": "+1-234-567-8900",
    "email": "john.doe@company.com",
    "company": "Tech Corp",
    "job_title": "Software Engineer",
    "website": "https://www.company.com",
    "address": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "USA",
    "notes": "Available Monday-Friday"
  },
  "size": 10,
  "border": 4,
  "error_correction": "H",
  "foreground_color": "black",
  "background_color": "white",
  "output_format": "png",
  "include_logo": false
}
```

**Response:**
```json
{
  "success": true,
  "message": "QR code generated successfully",
  "filename": "qr_abc123.png",
  "file_path": "/path/to/output/qr_abc123.png",
  "file_size": 12345,
  "format": "png"
}
```

**Status Codes:**
- `200 OK` - QR code generated successfully
- `422 Unprocessable Entity` - Invalid input data
- `500 Internal Server Error` - Generation failed

---

### 2. Generate QR Code with Logo

Generate a QR code with a custom logo.

**Endpoint:** `POST /generate-with-logo`

**Content-Type:** `multipart/form-data`

**Form Fields:**
- `business_card` (string, required) - JSON string of business card data
- `size` (integer, optional) - QR code size (default: 10)
- `border` (integer, optional) - Border size (default: 4)
- `error_correction` (string, optional) - Error correction level (default: H)
- `foreground_color` (string, optional) - Foreground color (default: black)
- `background_color` (string, optional) - Background color (default: white)
- `output_format` (string, optional) - Output format (default: png)
- `logo` (file, optional) - Logo image file

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/generate-with-logo" \
  -F "business_card={\"name\":\"John Doe\",\"email\":\"john@example.com\"}" \
  -F "size=10" \
  -F "output_format=png" \
  -F "logo=@/path/to/logo.png"
```

---

### 3. Batch Generate QR Codes

Generate multiple QR codes in a single request.

**Endpoint:** `POST /batch-generate`

**Request Body:**
```json
[
  {
    "business_card": {
      "name": "User 1",
      "email": "user1@example.com"
    },
    "output_format": "png"
  },
  {
    "business_card": {
      "name": "User 2",
      "email": "user2@example.com"
    },
    "output_format": "svg"
  }
]
```

**Response:**
```json
[
  {
    "success": true,
    "message": "QR code generated successfully",
    "filename": "qr_xyz789.png",
    "file_path": "/path/to/output/qr_xyz789.png",
    "file_size": 12345,
    "format": "png"
  },
  {
    "success": true,
    "message": "QR code generated successfully",
    "filename": "qr_def456.svg",
    "file_path": "/path/to/output/qr_def456.svg",
    "file_size": 6789,
    "format": "svg"
  }
]
```

**Limitations:**
- Maximum 100 QR codes per batch request

---

### 4. Download QR Code

Download a generated QR code file.

**Endpoint:** `GET /download/{filename}`

**Parameters:**
- `filename` (path parameter) - Name of the QR code file

**Response:**
- File download with appropriate content-type

**Status Codes:**
- `200 OK` - File downloaded successfully
- `404 Not Found` - File not found

---

### 5. Health Check

Check API health status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "IBQ QR Code Generator"
}
```

---

### 6. API Information

Get API information and available endpoints.

**Endpoint:** `GET /info`

**Response:**
```json
{
  "name": "IBQ QR Code Generator",
  "version": "1.0.0",
  "description": "QR Code Generator API for Business Cards",
  "endpoints": {
    "generate": "/api/v1/generate",
    "generate_with_logo": "/api/v1/generate-with-logo",
    "download": "/api/v1/download/{filename}",
    "batch_generate": "/api/v1/batch-generate",
    "health": "/api/v1/health"
  }
}
```

## Data Models

### BusinessCard

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Full name (1-100 characters) |
| phone | string | No | Phone number (max 20 characters) |
| email | string | No | Email address (valid email format) |
| company | string | No | Company name (max 100 characters) |
| job_title | string | No | Job title (max 100 characters) |
| website | string | No | Website URL |
| address | string | No | Physical address (max 200 characters) |
| city | string | No | City (max 50 characters) |
| state | string | No | State/Province (max 50 characters) |
| postal_code | string | No | Postal code (max 20 characters) |
| country | string | No | Country (max 50 characters) |
| notes | string | No | Additional notes (max 500 characters) |

### QRCodeRequest

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| business_card | BusinessCard | Yes | - | Business card information |
| size | integer | No | 10 | QR code box size (1-50) |
| border | integer | No | 4 | Border size in boxes (0-10) |
| error_correction | string | No | H | Error correction level (L, M, Q, H) |
| foreground_color | string | No | black | Foreground color |
| background_color | string | No | white | Background color |
| output_format | string | No | png | Output format (png, svg, pdf) |
| include_logo | boolean | No | false | Include logo in QR code |

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common error codes:
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Rate Limiting

Currently, there is no rate limiting. For production deployment, consider implementing rate limiting based on your needs.

## Examples

### Python

```python
import requests

# Generate QR code
response = requests.post(
    'http://localhost:8000/api/v1/generate',
    json={
        'business_card': {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1-555-0100'
        },
        'output_format': 'png'
    }
)

result = response.json()
print(f"QR code saved: {result['filename']}")

# Download the file
download_response = requests.get(
    f"http://localhost:8000/api/v1/download/{result['filename']}"
)
with open('qr_code.png', 'wb') as f:
    f.write(download_response.content)
```

### JavaScript

```javascript
// Generate QR code
fetch('http://localhost:8000/api/v1/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    business_card: {
      name: 'John Doe',
      email: 'john@example.com',
      phone: '+1-555-0100'
    },
    output_format: 'png'
  })
})
.then(response => response.json())
.then(data => {
  console.log('QR code generated:', data.filename);
  // Download the file
  window.location.href = `/api/v1/download/${data.filename}`;
});
```

### cURL

```bash
# Generate QR code
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "business_card": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "output_format": "png"
  }'

# Download QR code
curl -O "http://localhost:8000/api/v1/download/qr_abc123.png"
```

## Interactive Documentation

For interactive API documentation, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
