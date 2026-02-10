"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_info():
    """Test API info endpoint"""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_generate_qr_code():
    """Test QR code generation endpoint"""
    request_data = {
        "business_card": {
            "name": "Test User",
            "phone": "+1-555-0100",
            "email": "test@example.com",
            "company": "Test Corp"
        },
        "size": 10,
        "border": 4,
        "error_correction": "H",
        "foreground_color": "black",
        "background_color": "white",
        "output_format": "png",
        "include_logo": False
    }
    
    response = client.post("/api/v1/generate", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["filename"] is not None
    assert data["file_path"] is not None


def test_generate_qr_code_validation():
    """Test QR code generation with invalid data"""
    # Missing required field (name)
    request_data = {
        "business_card": {
            "phone": "+1-555-0100"
        },
        "output_format": "png"
    }
    
    response = client.post("/api/v1/generate", json=request_data)
    assert response.status_code == 422  # Validation error


def test_batch_generate():
    """Test batch QR code generation"""
    requests_data = [
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
    
    response = client.post("/api/v1/batch-generate", json=requests_data)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert all(result["success"] for result in data)


def test_home_page():
    """Test home page loads"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"IBQ QR Code Generator" in response.content
