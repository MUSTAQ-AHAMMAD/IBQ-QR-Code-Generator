"""
Core QR Code Generation Module
"""
import os
import io
import hashlib
from typing import Optional, Tuple
from pathlib import Path
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image
import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from app.core.vcard import VCardFormatter
from app.models.business_card import BusinessCard, QRCodeRequest
from app.config import get_settings


class QRCodeGenerator:
    """QR Code generator with business card support"""
    
    def __init__(self):
        self.settings = get_settings()
        self.cache = {}
        self._ensure_output_directory()
    
    def _ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        output_dir = Path(self.settings.output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_error_correction_level(self, level: str):
        """Get QR code error correction level"""
        levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H,
        }
        return levels.get(level.upper(), qrcode.constants.ERROR_CORRECT_H)
    
    def _generate_cache_key(self, request: QRCodeRequest) -> str:
        """Generate cache key from request"""
        data = f"{request.business_card.json()}{request.size}{request.border}{request.error_correction}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def _create_qr_code(self, data: str, request: QRCodeRequest) -> qrcode.QRCode:
        """Create QR code instance"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=self._get_error_correction_level(request.error_correction),
            box_size=request.size,
            border=request.border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr
    
    def _add_logo_to_image(self, img: Image.Image, logo_path: str) -> Image.Image:
        """Add logo to the center of QR code"""
        try:
            logo = Image.open(logo_path)
            
            # Calculate logo size (typically 1/5 of QR code size)
            qr_width, qr_height = img.size
            logo_size = min(qr_width, qr_height) // 5
            
            # Resize logo
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Create white background for logo
            logo_bg = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
            logo_bg_pos = ((logo_bg.size[0] - logo_size) // 2, (logo_bg.size[1] - logo_size) // 2)
            
            # Handle transparency
            if logo.mode == 'RGBA':
                logo_bg.paste(logo, logo_bg_pos, logo)
            else:
                logo_bg.paste(logo, logo_bg_pos)
            
            # Calculate position for logo
            logo_pos = ((qr_width - logo_bg.size[0]) // 2, (qr_height - logo_bg.size[1]) // 2)
            
            # Paste logo onto QR code
            img.paste(logo_bg, logo_pos)
            
            return img
        except Exception as e:
            # If logo fails, return original image
            print(f"Warning: Could not add logo: {e}")
            return img
    
    def generate_png(self, request: QRCodeRequest, logo_path: Optional[str] = None) -> Tuple[str, Path]:
        """
        Generate PNG QR code
        
        Args:
            request: QR code request
            logo_path: Optional path to logo image
            
        Returns:
            Tuple of (filename, file_path)
        """
        # Generate vCard data
        vcard_data = VCardFormatter.format(request.business_card)
        
        # Create QR code
        qr = self._create_qr_code(vcard_data, request)
        
        # Generate image with colors
        img = qr.make_image(
            fill_color=request.foreground_color,
            back_color=request.background_color
        )
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Add logo if requested
        if request.include_logo and logo_path and os.path.exists(logo_path):
            img = self._add_logo_to_image(img, logo_path)
        
        # Save image
        filename = f"qr_{self._generate_cache_key(request)}.png"
        file_path = Path(self.settings.output_directory) / filename
        img.save(file_path, 'PNG')
        
        return filename, file_path
    
    def generate_svg(self, request: QRCodeRequest) -> Tuple[str, Path]:
        """
        Generate SVG QR code
        
        Args:
            request: QR code request
            
        Returns:
            Tuple of (filename, file_path)
        """
        # Generate vCard data
        vcard_data = VCardFormatter.format(request.business_card)
        
        # Create QR code
        qr = self._create_qr_code(vcard_data, request)
        
        # Get QR code matrix
        matrix = qr.get_matrix()
        
        # Calculate dimensions
        box_size = request.size
        border = request.border
        width = (len(matrix[0]) + border * 2) * box_size
        height = (len(matrix) + border * 2) * box_size
        
        # Create SVG
        filename = f"qr_{self._generate_cache_key(request)}.svg"
        file_path = Path(self.settings.output_directory) / filename
        
        dwg = svgwrite.Drawing(str(file_path), size=(width, height))
        
        # Add background
        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=request.background_color))
        
        # Add QR code modules
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                if col:
                    x = (j + border) * box_size
                    y = (i + border) * box_size
                    dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), fill=request.foreground_color))
        
        dwg.save()
        
        return filename, file_path
    
    def generate_pdf(self, request: QRCodeRequest, logo_path: Optional[str] = None) -> Tuple[str, Path]:
        """
        Generate PDF QR code
        
        Args:
            request: QR code request
            logo_path: Optional path to logo image
            
        Returns:
            Tuple of (filename, file_path)
        """
        # First generate PNG
        png_filename, png_path = self.generate_png(request, logo_path)
        
        # Create PDF
        filename = f"qr_{self._generate_cache_key(request)}.pdf"
        file_path = Path(self.settings.output_directory) / filename
        
        # Create PDF with QR code
        c = canvas.Canvas(str(file_path), pagesize=letter)
        
        # Add title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "Business Card QR Code")
        
        # Add QR code image
        c.drawImage(str(png_path), 100, 400, width=300, height=300)
        
        # Add business card info
        c.setFont("Helvetica", 12)
        y_position = 350
        line_height = 20
        
        if request.business_card.name:
            c.drawString(100, y_position, f"Name: {request.business_card.name}")
            y_position -= line_height
        
        if request.business_card.job_title:
            c.drawString(100, y_position, f"Title: {request.business_card.job_title}")
            y_position -= line_height
        
        if request.business_card.company:
            c.drawString(100, y_position, f"Company: {request.business_card.company}")
            y_position -= line_height
        
        if request.business_card.phone:
            c.drawString(100, y_position, f"Phone: {request.business_card.phone}")
            y_position -= line_height
        
        if request.business_card.email:
            c.drawString(100, y_position, f"Email: {request.business_card.email}")
            y_position -= line_height
        
        if request.business_card.website:
            c.drawString(100, y_position, f"Website: {request.business_card.website}")
        
        c.save()
        
        # Clean up temporary PNG if not needed
        # Keep it for now as it might be useful
        
        return filename, file_path
    
    def generate(self, request: QRCodeRequest, logo_path: Optional[str] = None) -> Tuple[str, Path]:
        """
        Generate QR code in requested format
        
        Args:
            request: QR code request
            logo_path: Optional path to logo image
            
        Returns:
            Tuple of (filename, file_path)
        """
        # Check cache if enabled
        if self.settings.enable_cache:
            cache_key = self._generate_cache_key(request)
            if cache_key in self.cache:
                return self.cache[cache_key]
        
        # Generate based on format
        if request.output_format.lower() == 'png':
            result = self.generate_png(request, logo_path)
        elif request.output_format.lower() == 'svg':
            result = self.generate_svg(request)
        elif request.output_format.lower() == 'pdf':
            result = self.generate_pdf(request, logo_path)
        else:
            raise ValueError(f"Unsupported output format: {request.output_format}")
        
        # Cache result
        if self.settings.enable_cache:
            self.cache[cache_key] = result
        
        return result
