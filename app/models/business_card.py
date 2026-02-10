"""
Data models for business card QR codes
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class BusinessCard(BaseModel):
    """Business card information model"""
    name: str = Field(..., min_length=1, max_length=100, description="Full name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    company: Optional[str] = Field(None, max_length=100, description="Company name")
    job_title: Optional[str] = Field(None, max_length=100, description="Job title")
    website: Optional[str] = Field(None, description="Website URL")
    address: Optional[str] = Field(None, max_length=200, description="Physical address")
    city: Optional[str] = Field(None, max_length=50, description="City")
    state: Optional[str] = Field(None, max_length=50, description="State/Province")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal code")
    country: Optional[str] = Field(None, max_length=50, description="Country")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")
    
    class Config:
        json_schema_extra = {
            "example": {
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
            }
        }


class QRCodeRequest(BaseModel):
    """QR Code generation request"""
    business_card: BusinessCard
    size: int = Field(10, ge=1, le=50, description="QR code box size")
    border: int = Field(4, ge=0, le=10, description="Border size in boxes")
    error_correction: str = Field("H", pattern="^[LMQH]$", description="Error correction level (L, M, Q, H)")
    foreground_color: str = Field("black", description="Foreground color (hex or name)")
    background_color: str = Field("white", description="Background color (hex or name)")
    output_format: str = Field("png", pattern="^(png|svg|pdf)$", description="Output format")
    include_logo: bool = Field(False, description="Include a logo in the center")
    
    class Config:
        json_schema_extra = {
            "example": {
                "business_card": {
                    "name": "John Doe",
                    "phone": "+1-234-567-8900",
                    "email": "john.doe@company.com",
                    "company": "Tech Corp",
                    "job_title": "Software Engineer"
                },
                "size": 10,
                "border": 4,
                "error_correction": "H",
                "foreground_color": "black",
                "background_color": "white",
                "output_format": "png",
                "include_logo": False
            }
        }


class QRCodeResponse(BaseModel):
    """QR Code generation response"""
    success: bool
    message: str
    filename: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    format: Optional[str] = None
