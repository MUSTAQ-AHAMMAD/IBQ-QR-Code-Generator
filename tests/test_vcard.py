"""
Unit tests for vCard formatter
"""
import pytest
from app.models.business_card import BusinessCard
from app.core.vcard import VCardFormatter


def test_vcard_formatter_basic():
    """Test basic vCard generation"""
    card = BusinessCard(
        name="John Doe",
        phone="+1-234-567-8900",
        email="john@example.com"
    )
    
    vcard = VCardFormatter.format(card)
    
    assert "BEGIN:VCARD" in vcard
    assert "VERSION:3.0" in vcard
    assert "FN:John Doe" in vcard
    assert "TEL;TYPE=WORK,VOICE:+1-234-567-8900" in vcard
    assert "EMAIL;TYPE=WORK,INTERNET:john@example.com" in vcard
    assert "END:VCARD" in vcard


def test_vcard_formatter_full_details():
    """Test vCard generation with all fields"""
    card = BusinessCard(
        name="Jane Smith",
        phone="+1-555-0100",
        email="jane.smith@company.com",
        company="Tech Corp",
        job_title="Software Engineer",
        website="https://www.company.com",
        address="123 Main St",
        city="New York",
        state="NY",
        postal_code="10001",
        country="USA",
        notes="Available weekdays"
    )
    
    vcard = VCardFormatter.format(card)
    
    assert "FN:Jane Smith" in vcard
    assert "ORG:Tech Corp" in vcard
    assert "TITLE:Software Engineer" in vcard
    assert "URL:https://www.company.com" in vcard
    assert "ADR;TYPE=WORK:" in vcard
    assert "NOTE:Available weekdays" in vcard


def test_vcard_validator():
    """Test vCard validation"""
    card = BusinessCard(name="Test User", email="test@example.com")
    vcard = VCardFormatter.format(card)
    
    assert VCardFormatter.validate(vcard) is True
    
    # Test invalid vCard
    invalid_vcard = "BEGIN:VCARD\nVERSION:3.0"
    assert VCardFormatter.validate(invalid_vcard) is False
