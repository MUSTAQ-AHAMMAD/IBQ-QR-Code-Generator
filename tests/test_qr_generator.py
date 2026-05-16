"""
Unit tests for QR code generator
"""
import pytest
from pathlib import Path
import os

from app.models.business_card import BusinessCard, QRCodeRequest
from app.core.qr_generator import QRCodeGenerator


@pytest.fixture
def sample_card():
    """Sample business card for testing"""
    return BusinessCard(
        name="Test User",
        phone="+1-555-0100",
        email="test@example.com",
        company="Test Company",
        job_title="Tester"
    )


@pytest.fixture
def qr_generator():
    """QR code generator instance"""
    return QRCodeGenerator()


def test_generate_png(qr_generator, sample_card):
    """Test PNG QR code generation"""
    request = QRCodeRequest(
        business_card=sample_card,
        size=10,
        border=4,
        error_correction="H",
        output_format="png"
    )
    
    filename, file_path = qr_generator.generate_png(request)
    
    assert filename.endswith('.png')
    assert file_path.exists()
    assert file_path.stat().st_size > 0
    
    # Cleanup
    if file_path.exists():
        os.remove(file_path)


def test_generate_svg(qr_generator, sample_card):
    """Test SVG QR code generation"""
    request = QRCodeRequest(
        business_card=sample_card,
        size=10,
        border=4,
        error_correction="H",
        output_format="svg"
    )
    
    filename, file_path = qr_generator.generate_svg(request)
    
    assert filename.endswith('.svg')
    assert file_path.exists()
    assert file_path.stat().st_size > 0
    
    # Cleanup
    if file_path.exists():
        os.remove(file_path)


def test_generate_pdf(qr_generator, sample_card):
    """Test PDF QR code generation"""
    request = QRCodeRequest(
        business_card=sample_card,
        size=10,
        border=4,
        error_correction="H",
        output_format="pdf"
    )
    
    filename, file_path = qr_generator.generate_pdf(request)
    
    assert filename.endswith('.pdf')
    assert file_path.exists()
    assert file_path.stat().st_size > 0
    
    # Cleanup
    if file_path.exists():
        os.remove(file_path)
    
    # Also cleanup PNG that was generated
    png_path = file_path.parent / filename.replace('.pdf', '.png')
    if png_path.exists():
        os.remove(png_path)


def test_error_correction_levels(qr_generator, sample_card):
    """Test different error correction levels"""
    for level in ['L', 'M', 'Q', 'H']:
        request = QRCodeRequest(
            business_card=sample_card,
            error_correction=level,
            output_format="png"
        )
        
        filename, file_path = qr_generator.generate_png(request)
        assert file_path.exists()
        
        # Cleanup
        if file_path.exists():
            os.remove(file_path)


def test_customization(qr_generator, sample_card):
    """Test QR code customization"""
    request = QRCodeRequest(
        business_card=sample_card,
        size=15,
        border=2,
        foreground_color="#0000ff",
        background_color="#ffff00",
        output_format="png"
    )
    
    filename, file_path = qr_generator.generate_png(request)
    
    assert file_path.exists()
    assert file_path.stat().st_size > 0
    
    # Cleanup
    if file_path.exists():
        os.remove(file_path)
