"""
API endpoints for QR code generation
"""
import os
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
import json

from app.models.business_card import BusinessCard, QRCodeRequest, QRCodeResponse
from app.core.qr_generator import QRCodeGenerator
from app.config import get_settings

router = APIRouter(prefix="/api/v1", tags=["qr-codes"])
settings = get_settings()
qr_generator = QRCodeGenerator()


@router.post("/generate", response_model=QRCodeResponse)
async def generate_qr_code(request: QRCodeRequest):
    """
    Generate a QR code from business card information
    
    Args:
        request: QR code generation request with business card data
        
    Returns:
        QRCodeResponse with file information
    """
    try:
        filename, file_path = qr_generator.generate(request)
        file_size = os.path.getsize(file_path)
        
        return QRCodeResponse(
            success=True,
            message="QR code generated successfully",
            filename=filename,
            file_path=str(file_path),
            file_size=file_size,
            format=request.output_format
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QR code: {str(e)}")


@router.post("/generate-with-logo", response_model=QRCodeResponse)
async def generate_qr_code_with_logo(
    business_card: str = Form(...),
    size: int = Form(10),
    border: int = Form(4),
    error_correction: str = Form("H"),
    foreground_color: str = Form("black"),
    background_color: str = Form("white"),
    output_format: str = Form("png"),
    logo: Optional[UploadFile] = File(None)
):
    """
    Generate a QR code with an optional logo
    
    Args:
        business_card: JSON string of business card data
        size: QR code box size
        border: Border size
        error_correction: Error correction level
        foreground_color: Foreground color
        background_color: Background color
        output_format: Output format (png, svg, pdf)
        logo: Optional logo image file
        
    Returns:
        QRCodeResponse with file information
    """
    try:
        # Parse business card JSON
        card_data = json.loads(business_card)
        card = BusinessCard(**card_data)
        
        # Create request
        request = QRCodeRequest(
            business_card=card,
            size=size,
            border=border,
            error_correction=error_correction,
            foreground_color=foreground_color,
            background_color=background_color,
            output_format=output_format,
            include_logo=logo is not None
        )
        
        # Handle logo upload
        logo_path = None
        if logo:
            # Validate file size
            content = await logo.read()
            if len(content) > settings.max_logo_size_mb * 1024 * 1024:
                raise HTTPException(status_code=400, detail=f"Logo file too large. Maximum size: {settings.max_logo_size_mb}MB")
            
            # Save logo temporarily
            logo_path = Path(settings.output_directory) / f"temp_logo_{logo.filename}"
            with open(logo_path, "wb") as f:
                f.write(content)
        
        # Generate QR code
        filename, file_path = qr_generator.generate(request, str(logo_path) if logo_path else None)
        file_size = os.path.getsize(file_path)
        
        # Clean up temporary logo
        if logo_path and logo_path.exists():
            os.remove(logo_path)
        
        return QRCodeResponse(
            success=True,
            message="QR code generated successfully",
            filename=filename,
            file_path=str(file_path),
            file_size=file_size,
            format=request.output_format
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid business card JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QR code: {str(e)}")


@router.get("/download/{filename}")
async def download_qr_code(filename: str):
    """
    Download a generated QR code
    
    Args:
        filename: Name of the QR code file
        
    Returns:
        File download response
    """
    file_path = Path(settings.output_directory) / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get media type based on extension
    media_types = {
        '.png': 'image/png',
        '.svg': 'image/svg+xml',
        '.pdf': 'application/pdf'
    }
    media_type = media_types.get(file_path.suffix, 'application/octet-stream')
    
    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        filename=filename
    )


@router.post("/batch-generate", response_model=list[QRCodeResponse])
async def batch_generate_qr_codes(requests: list[QRCodeRequest]):
    """
    Generate multiple QR codes in batch
    
    Args:
        requests: List of QR code generation requests
        
    Returns:
        List of QRCodeResponse objects
    """
    if len(requests) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 QR codes per batch request")
    
    results = []
    for request in requests:
        try:
            filename, file_path = qr_generator.generate(request)
            file_size = os.path.getsize(file_path)
            
            results.append(QRCodeResponse(
                success=True,
                message="QR code generated successfully",
                filename=filename,
                file_path=str(file_path),
                file_size=file_size,
                format=request.output_format
            ))
        except Exception as e:
            results.append(QRCodeResponse(
                success=False,
                message=f"Failed to generate QR code: {str(e)}",
                filename=None,
                file_path=None,
                file_size=None,
                format=request.output_format
            ))
    
    return results


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "IBQ QR Code Generator"}
