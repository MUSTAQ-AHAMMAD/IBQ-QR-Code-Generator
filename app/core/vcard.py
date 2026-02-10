"""
vCard formatter for business cards
"""
from typing import Optional
from app.models.business_card import BusinessCard


class VCardFormatter:
    """Format business card data as vCard 3.0"""
    
    @staticmethod
    def format(card: BusinessCard) -> str:
        """
        Generate vCard format string from business card data
        
        Args:
            card: BusinessCard instance
            
        Returns:
            vCard formatted string
        """
        vcard_lines = [
            "BEGIN:VCARD",
            "VERSION:3.0"
        ]
        
        # Name (required)
        if card.name:
            # Format: N:LastName;FirstName;MiddleName;Prefix;Suffix
            name_parts = card.name.split()
            if len(name_parts) >= 2:
                last_name = name_parts[-1]
                first_name = " ".join(name_parts[:-1])
                vcard_lines.append(f"N:{last_name};{first_name};;;")
            else:
                vcard_lines.append(f"N:{card.name};;;;")
            vcard_lines.append(f"FN:{card.name}")
        
        # Organization and title
        if card.company:
            vcard_lines.append(f"ORG:{card.company}")
        
        if card.job_title:
            vcard_lines.append(f"TITLE:{card.job_title}")
        
        # Phone
        if card.phone:
            vcard_lines.append(f"TEL;TYPE=WORK,VOICE:{card.phone}")
        
        # Email
        if card.email:
            vcard_lines.append(f"EMAIL;TYPE=WORK,INTERNET:{card.email}")
        
        # Website
        if card.website:
            vcard_lines.append(f"URL:{card.website}")
        
        # Address
        if any([card.address, card.city, card.state, card.postal_code, card.country]):
            # Format: ADR;TYPE=WORK:;;Street;City;State;PostalCode;Country
            address_parts = [
                "",  # P.O. Box
                "",  # Extended address
                card.address or "",
                card.city or "",
                card.state or "",
                card.postal_code or "",
                card.country or ""
            ]
            vcard_lines.append(f"ADR;TYPE=WORK:{';'.join(address_parts)}")
        
        # Notes
        if card.notes:
            vcard_lines.append(f"NOTE:{card.notes}")
        
        # End vCard
        vcard_lines.append("END:VCARD")
        
        return "\n".join(vcard_lines)
    
    @staticmethod
    def validate(vcard: str) -> bool:
        """
        Validate vCard format
        
        Args:
            vcard: vCard string
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["BEGIN:VCARD", "VERSION:", "FN:", "END:VCARD"]
        return all(field in vcard for field in required_fields)
