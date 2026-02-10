"""
Utility functions for QR code generation and management.
"""
import os
import qrcode
from qrcode.image.svg import SvgPathImage
from PIL import Image
from io import BytesIO
import base64
from datetime import datetime

def generate_vcard(contact_data):
    """
    Generate vCard format string from contact data.
    
    Args:
        contact_data: Dictionary with contact information
        
    Returns:
        vCard formatted string
    """
    vcard_lines = ['BEGIN:VCARD', 'VERSION:3.0']
    
    # Name
    if contact_data.get('contact_name'):
        name_parts = contact_data['contact_name'].split(' ', 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        vcard_lines.append(f'N:{last_name};{first_name};;;')
        vcard_lines.append(f'FN:{contact_data["contact_name"]}')
    
    # Title and Organization
    if contact_data.get('contact_title'):
        vcard_lines.append(f'TITLE:{contact_data["contact_title"]}')
    
    if contact_data.get('contact_company'):
        vcard_lines.append(f'ORG:{contact_data["contact_company"]}')
    
    # Contact information
    if contact_data.get('contact_phone'):
        vcard_lines.append(f'TEL;TYPE=WORK,VOICE:{contact_data["contact_phone"]}')
    
    if contact_data.get('contact_email'):
        vcard_lines.append(f'EMAIL;TYPE=INTERNET:{contact_data["contact_email"]}')
    
    if contact_data.get('contact_website'):
        vcard_lines.append(f'URL:{contact_data["contact_website"]}')
    
    # Address
    if contact_data.get('contact_address'):
        # Format: ADR;TYPE=WORK:;;street;city;state;postal;country
        address = contact_data['contact_address'].replace('\n', ' ').replace('\r', '')
        vcard_lines.append(f'ADR;TYPE=WORK:;;{address};;;;')
    
    vcard_lines.append('END:VCARD')
    
    return '\n'.join(vcard_lines)

def create_qr_code(data, settings=None):
    """
    Create a QR code image with advanced styling options.
    
    Args:
        data: Data to encode in the QR code
        settings: Dictionary with QR code settings
        
    Returns:
        PIL Image object
    """
    if settings is None:
        settings = {}
    
    # Get settings with defaults
    error_correction_map = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H,
    }
    
    error_correction = error_correction_map.get(settings.get('error_correction', 'H'), qrcode.constants.ERROR_CORRECT_H)
    box_size = settings.get('box_size', 10)
    border = settings.get('border', 4)
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image
    fill_color = settings.get('foreground_color', '#000000')
    back_color = settings.get('background_color', '#FFFFFF')
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Resize if needed
    size = settings.get('size', 300)
    if size:
        img = img.resize((size, size), Image.LANCZOS)
    
    # Apply gradient if enabled (basic implementation using PIL)
    if settings.get('gradient_enabled') and settings.get('gradient_color'):
        img = apply_gradient_effect(img, fill_color, settings.get('gradient_color'), settings.get('gradient_type', 'linear'))
    
    # Apply style effects (rounded corners, dots, etc.)
    qr_style = settings.get('qr_style', 'square')
    if qr_style in ['rounded', 'dots', 'circles']:
        img = apply_style_effect(img, qr_style, back_color)
    
    # Add logo if provided
    logo_path = settings.get('logo_path')
    if logo_path and os.path.exists(logo_path):
        img = add_logo_to_qr(img, logo_path)
    
    # Add frame if specified
    frame_style = settings.get('frame_style')
    if frame_style and frame_style != 'none':
        img = add_frame_to_qr(img, frame_style, settings.get('frame_text'), settings.get('frame_color', '#000000'), back_color)
    
    return img

def create_qr_code_svg(data, settings=None):
    """
    Create a QR code in SVG format.
    
    Args:
        data: Data to encode in the QR code
        settings: Dictionary with QR code settings
        
    Returns:
        SVG string
    """
    if settings is None:
        settings = {}
    
    error_correction_map = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H,
    }
    
    error_correction = error_correction_map.get(settings.get('error_correction', 'H'), qrcode.constants.ERROR_CORRECT_H)
    border = settings.get('border', 4)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=10,
        border=border,
        image_factory=SvgPathImage
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=settings.get('foreground_color', '#000000'),
                        back_color=settings.get('background_color', '#FFFFFF'))
    
    return img

def add_logo_to_qr(qr_img, logo_path, logo_size_ratio=0.3):
    """
    Add a logo to the center of a QR code.
    
    Args:
        qr_img: PIL Image object of the QR code
        logo_path: Path to the logo image file
        logo_size_ratio: Ratio of logo size to QR code size
        
    Returns:
        PIL Image object with logo
    """
    try:
        logo = Image.open(logo_path)
        
        # Calculate logo size
        qr_width, qr_height = qr_img.size
        logo_size = int(min(qr_width, qr_height) * logo_size_ratio)
        
        # Resize logo
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        
        # Add white background to logo
        logo_bg = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
        logo_bg.paste(logo, (10, 10))
        
        # Calculate position
        logo_pos = (
            (qr_width - logo_bg.size[0]) // 2,
            (qr_height - logo_bg.size[1]) // 2
        )
        
        # Convert QR code to RGB if necessary
        if qr_img.mode != 'RGB':
            qr_img = qr_img.convert('RGB')
        
        # Paste logo
        qr_img.paste(logo_bg, logo_pos)
        
        return qr_img
    except Exception as e:
        print(f"Error adding logo: {e}")
        return qr_img

def save_qr_code(img, filepath, file_format='PNG'):
    """
    Save QR code image to file.
    
    Args:
        img: PIL Image object or SVG image
        filepath: Path where to save the file
        file_format: Format to save (PNG, SVG, PDF)
        
    Returns:
        File size in bytes
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if file_format.upper() == 'SVG':
        # SVG image
        with open(filepath, 'wb') as f:
            img.save(f)
        return os.path.getsize(filepath)
    elif file_format.upper() == 'PDF':
        # Convert to PDF
        img_rgb = img.convert('RGB')
        img_rgb.save(filepath, 'PDF')
        return os.path.getsize(filepath)
    else:
        # PNG or other formats
        img.save(filepath, file_format.upper())
        return os.path.getsize(filepath)

def generate_filename(name, file_format='png'):
    """
    Generate a unique filename for a QR code.
    
    Args:
        name: Base name for the file
        file_format: File extension
        
    Returns:
        Filename string
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).strip()
    safe_name = safe_name.replace(' ', '_')[:50]
    return f"{safe_name}_{timestamp}.{file_format}"

def get_qr_code_base64(img):
    """
    Convert QR code image to base64 string for preview.
    
    Args:
        img: PIL Image object
        
    Returns:
        Base64 encoded string
    """
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def validate_color(color):
    """
    Validate hex color format.
    
    Args:
        color: Color string
        
    Returns:
        Boolean indicating if color is valid
    """
    if not color or not isinstance(color, str):
        return False
    
    if not color.startswith('#'):
        return False
    
    if len(color) not in [4, 7]:  # #RGB or #RRGGBB
        return False
    
    try:
        int(color[1:], 16)
        return True
    except ValueError:
        return False

def generate_url_data(url):
    """
    Generate URL QR code data.
    
    Args:
        url: URL string
        
    Returns:
        URL string
    """
    return url

def generate_text_data(text):
    """
    Generate plain text QR code data.
    
    Args:
        text: Text string
        
    Returns:
        Text string
    """
    return text

def generate_email_data(email_data):
    """
    Generate email QR code data (mailto format).
    
    Args:
        email_data: Dictionary with email information
        
    Returns:
        mailto URL string
    """
    from urllib.parse import quote
    
    email = email_data.get('email_address', '')
    subject = email_data.get('email_subject', '')
    body = email_data.get('email_body', '')
    
    mailto = f'mailto:{email}'
    params = []
    
    if subject:
        params.append(f'subject={quote(subject)}')
    if body:
        params.append(f'body={quote(body)}')
    
    if params:
        mailto += '?' + '&'.join(params)
    
    return mailto

def generate_sms_data(sms_data):
    """
    Generate SMS QR code data.
    
    Args:
        sms_data: Dictionary with SMS information
        
    Returns:
        SMS URL string
    """
    phone = sms_data.get('sms_phone', '')
    message = sms_data.get('sms_message', '')
    
    if message:
        return f'SMSTO:{phone}:{message}'
    else:
        return f'SMSTO:{phone}'

def generate_phone_data(phone):
    """
    Generate phone QR code data.
    
    Args:
        phone: Phone number string
        
    Returns:
        Tel URL string
    """
    return f'tel:{phone}'

def generate_wifi_data(wifi_data):
    """
    Generate WiFi QR code data.
    
    Args:
        wifi_data: Dictionary with WiFi information
        
    Returns:
        WiFi configuration string
    """
    ssid = wifi_data.get('wifi_ssid', '')
    password = wifi_data.get('wifi_password', '')
    encryption = wifi_data.get('wifi_encryption', 'WPA')
    hidden = wifi_data.get('wifi_hidden', False)
    
    # WIFI:T:WPA;S:mynetwork;P:mypass;H:false;;
    wifi_string = f'WIFI:T:{encryption};S:{ssid};'
    
    if encryption != 'nopass' and password:
        wifi_string += f'P:{password};'
    
    wifi_string += f'H:{"true" if hidden else "false"};;'
    
    return wifi_string

def generate_social_data(platform, url):
    """
    Generate social media QR code data.
    
    Args:
        platform: Social media platform name
        url: Profile URL
        
    Returns:
        URL string
    """
    return url

def generate_app_store_data(url):
    """
    Generate app store QR code data.
    
    Args:
        url: App store URL
        
    Returns:
        URL string
    """
    return url

def generate_event_data(event_data):
    """
    Generate calendar event QR code data (iCal format).
    
    Args:
        event_data: Dictionary with event information
        
    Returns:
        iCal formatted string
    """
    from datetime import datetime
    
    title = event_data.get('event_title', '')
    location = event_data.get('event_location', '')
    start = event_data.get('event_start', '')
    end = event_data.get('event_end', '')
    description = event_data.get('event_description', '')
    
    # Basic iCal format
    ical_lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'BEGIN:VEVENT'
    ]
    
    if title:
        ical_lines.append(f'SUMMARY:{title}')
    
    if location:
        ical_lines.append(f'LOCATION:{location}')
    
    if description:
        ical_lines.append(f'DESCRIPTION:{description}')
    
    if start:
        # Convert to iCal format (YYYYMMDDTHHMMSS)
        try:
            dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            ical_lines.append(f'DTSTART:{dt.strftime("%Y%m%dT%H%M%S")}')
        except (ValueError, AttributeError):
            pass
    
    if end:
        try:
            dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            ical_lines.append(f'DTEND:{dt.strftime("%Y%m%dT%H%M%S")}')
        except (ValueError, AttributeError):
            pass
    
    ical_lines.extend([
        'END:VEVENT',
        'END:VCALENDAR'
    ])
    
    return '\n'.join(ical_lines)

def generate_location_data(location_data):
    """
    Generate location/map QR code data (geo URI).
    
    Args:
        location_data: Dictionary with location information
        
    Returns:
        Geo URI string
    """
    from urllib.parse import quote
    
    latitude = location_data.get('location_latitude', '')
    longitude = location_data.get('location_longitude', '')
    name = location_data.get('location_name', '')
    
    if latitude and longitude:
        geo_uri = f'geo:{latitude},{longitude}'
        if name:
            geo_uri += f'?q={latitude},{longitude}({quote(name)})'
        return geo_uri
    
    return ''

def generate_qr_data(qr_type, form_data):
    """
    Generate QR code data based on type.
    
    Args:
        qr_type: Type of QR code
        form_data: Form data dictionary
        
    Returns:
        QR code data string
    """
    if qr_type == 'vcard':
        return generate_vcard(form_data)
    elif qr_type == 'url':
        return generate_url_data(form_data.get('url', ''))
    elif qr_type == 'text':
        return generate_text_data(form_data.get('text_content', ''))
    elif qr_type == 'email':
        return generate_email_data(form_data)
    elif qr_type == 'sms':
        return generate_sms_data(form_data)
    elif qr_type == 'phone':
        return generate_phone_data(form_data.get('phone_number', ''))
    elif qr_type == 'wifi':
        return generate_wifi_data(form_data)
    elif qr_type in ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube']:
        return generate_social_data(qr_type, form_data.get('social_url', ''))
    elif qr_type in ['app_store', 'google_play']:
        return generate_app_store_data(form_data.get('app_url', ''))
    elif qr_type == 'event':
        return generate_event_data(form_data)
    elif qr_type == 'location':
        return generate_location_data(form_data)
    else:
        return ''

def apply_gradient_effect(img, color1, color2, gradient_type='linear'):
    """
    Apply a gradient effect to QR code foreground.
    
    Args:
        img: PIL Image object
        color1: Starting color (hex)
        color2: Ending color (hex)
        gradient_type: Type of gradient ('linear' or 'radial')
        
    Returns:
        PIL Image object with gradient
    """
    try:
        from PIL import ImageDraw
        
        # Convert to RGBA for manipulation
        img = img.convert('RGBA')
        width, height = img.size
        
        # Create a gradient overlay
        gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)
        
        # Parse colors
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        # Create gradient
        if gradient_type == 'linear':
            # Linear gradient from top to bottom
            for y in range(height):
                ratio = y / height
                r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * ratio)
                g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * ratio)
                b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        else:  # radial
            # Radial gradient from center
            center_x, center_y = width // 2, height // 2
            max_dist = ((width // 2) ** 2 + (height // 2) ** 2) ** 0.5
            
            for y in range(height):
                for x in range(width):
                    # Calculate distance from center
                    dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    ratio = min(dist / max_dist, 1.0)
                    
                    r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * ratio)
                    g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * ratio)
                    b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * ratio)
                    
                    gradient.putpixel((x, y), (r, g, b, 255))
        
        # Get QR code pixels
        pixels = img.load()
        grad_pixels = gradient.load()
        
        # Apply gradient only to dark pixels
        for y in range(height):
            for x in range(width):
                if pixels[x, y][0] < 128:  # Dark pixel
                    pixels[x, y] = grad_pixels[x, y]
        
        return img.convert('RGB')
    except Exception as e:
        print(f"Error applying gradient: {e}")
        return img.convert('RGB')

def apply_style_effect(img, style, background_color):
    """
    Apply style effects to QR code (rounded, dots, circles).
    
    Args:
        img: PIL Image object
        style: Style type ('rounded', 'dots', 'circles')
        background_color: Background color
        
    Returns:
        PIL Image object with style applied
    """
    try:
        from PIL import ImageDraw
        
        # For basic implementation, we'll just round corners of the entire QR code
        if style == 'rounded':
            img = img.convert('RGBA')
            width, height = img.size
            
            # Create a rounded rectangle mask
            mask = Image.new('L', (width, height), 0)
            draw = ImageDraw.Draw(mask)
            radius = min(width, height) // 20  # 5% radius
            draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=255)
            
            # Apply mask
            img.putalpha(mask)
            
            # Create background
            bg = Image.new('RGB', (width, height), background_color)
            bg.paste(img, (0, 0), img)
            return bg
        
        # For dots and circles, return original image
        # (Full implementation would require pixel-level manipulation)
        return img.convert('RGB')
    except Exception as e:
        print(f"Error applying style: {e}")
        return img.convert('RGB')

def get_default_font(size=20):
    """
    Get a default font that works across platforms.
    
    Args:
        size: Font size
        
    Returns:
        PIL ImageFont object
    """
    from PIL import ImageFont
    
    # Try common font paths for different platforms
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
        "/System/Library/Fonts/Helvetica.ttc",  # macOS
        "C:\\Windows\\Fonts\\arial.ttf",  # Windows
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",  # Linux alternative
    ]
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except Exception:
            continue
    
    # Fallback to default font
    return ImageFont.load_default()

def add_frame_to_qr(img, frame_style, frame_text, frame_color, background_color):
    """
    Add a frame around the QR code.
    
    Args:
        img: PIL Image object
        frame_style: Style of frame ('basic', 'banner', 'bottom-text')
        frame_text: Text to display in frame
        frame_color: Color of frame and text
        background_color: Background color
        
    Returns:
        PIL Image object with frame
    """
    try:
        from PIL import ImageDraw
        
        img = img.convert('RGB')
        width, height = img.size
        
        if frame_style == 'basic':
            # Add a simple border frame
            frame_width = 20
            new_size = (width + frame_width * 2, height + frame_width * 2)
            framed = Image.new('RGB', new_size, frame_color)
            framed.paste(img, (frame_width, frame_width))
            return framed
        
        elif frame_style == 'banner':
            # Add a banner at the top with text
            banner_height = 60
            new_size = (width, height + banner_height)
            framed = Image.new('RGB', new_size, background_color)
            
            # Draw banner
            draw = ImageDraw.Draw(framed)
            draw.rectangle([(0, 0), (width, banner_height)], fill=frame_color)
            
            # Add text
            if frame_text:
                font = get_default_font(24)
                
                # Calculate text position (centered)
                bbox = draw.textbbox((0, 0), frame_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_x = (width - text_width) // 2
                text_y = (banner_height - (bbox[3] - bbox[1])) // 2
                
                # Draw text in white
                draw.text((text_x, text_y), frame_text, fill='white', font=font)
            
            # Paste QR code below banner
            framed.paste(img, (0, banner_height))
            return framed
        
        elif frame_style == 'bottom-text':
            # Add text at the bottom
            text_height = 50
            new_size = (width, height + text_height)
            framed = Image.new('RGB', new_size, background_color)
            
            # Paste QR code at top
            framed.paste(img, (0, 0))
            
            # Add text at bottom
            if frame_text:
                draw = ImageDraw.Draw(framed)
                font = get_default_font(20)
                
                # Calculate text position (centered)
                bbox = draw.textbbox((0, 0), frame_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_x = (width - text_width) // 2
                text_y = height + (text_height - (bbox[3] - bbox[1])) // 2
                
                draw.text((text_x, text_y), frame_text, fill=frame_color, font=font)
            
            return framed
        
        return img
    except Exception as e:
        print(f"Error adding frame: {e}")
        return img
