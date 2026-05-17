"""
Analytics service for QR code scan tracking.
Tracks device information, location, and provides analytics data.
"""
from flask import request
from models import db, QRScan, QRCode
from datetime import datetime, timedelta
from sqlalchemy import func
import user_agents
import secrets

class AnalyticsService:
    """Service for tracking and analyzing QR code scans."""

    @staticmethod
    def track_scan(qr_code_id):
        """
        Track a QR code scan with comprehensive analytics data.

        Args:
            qr_code_id: ID of the QR code being scanned

        Returns:
            QRScan: The created scan record
        """
        # Get device and browser information
        user_agent_string = request.headers.get('User-Agent', '')
        user_agent = user_agents.parse(user_agent_string)

        # Determine device type
        if user_agent.is_mobile:
            device_type = 'mobile'
        elif user_agent.is_tablet:
            device_type = 'tablet'
        else:
            device_type = 'desktop'

        # Get OS and browser
        operating_system = user_agent.os.family
        browser = user_agent.browser.family

        # Get IP address
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For').split(',')[0].strip()

        # Get referrer information
        referrer_url = request.referrer
        referrer_domain = None
        if referrer_url:
            from urllib.parse import urlparse
            parsed = urlparse(referrer_url)
            referrer_domain = parsed.netloc

        # Get or create session ID for tracking repeat scans
        session_id = request.cookies.get('analytics_session')
        if not session_id:
            session_id = secrets.token_urlsafe(32)

        # Check if this is a unique scan (first scan from this session)
        existing_scan = QRScan.query.filter_by(
            qr_code_id=qr_code_id,
            session_id=session_id
        ).first()

        is_unique = existing_scan is None

        # Get location data (requires external service like ip-api.com or MaxMind)
        # For now, we'll leave these as None - implement with your preferred geolocation service
        country = None
        city = None
        latitude = None
        longitude = None

        # Optionally integrate with geolocation API
        try:
            location_data = AnalyticsService._get_location_from_ip(ip_address)
            if location_data:
                country = location_data.get('country')
                city = location_data.get('city')
                latitude = location_data.get('latitude')
                longitude = location_data.get('longitude')
        except:
            pass  # Geolocation is optional

        # Create scan record
        scan = QRScan(
            qr_code_id=qr_code_id,
            device_type=device_type,
            operating_system=operating_system,
            browser=browser,
            user_agent=user_agent_string[:500],  # Truncate to fit column
            ip_address=ip_address,
            country=country,
            city=city,
            latitude=latitude,
            longitude=longitude,
            referrer_url=referrer_url[:500] if referrer_url else None,
            referrer_domain=referrer_domain,
            session_id=session_id,
            is_unique=is_unique
        )

        db.session.add(scan)

        # Update QR code view count
        qr_code = QRCode.query.get(qr_code_id)
        if qr_code:
            qr_code.view_count += 1

        db.session.commit()

        return scan

    @staticmethod
    def _get_location_from_ip(ip_address):
        """
        Get location data from IP address.
        Implement this with your preferred geolocation service (ip-api, MaxMind, etc.)

        Returns:
            dict: Location data or None
        """
        # Example implementation with ip-api.com (free tier)
        # Uncomment and adjust if you want to use this service
        """
        import requests
        try:
            response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'country': data.get('country'),
                        'city': data.get('city'),
                        'latitude': data.get('lat'),
                        'longitude': data.get('lon')
                    }
        except:
            pass
        """
        return None

    @staticmethod
    def get_qr_analytics(qr_code_id, days=30):
        """
        Get analytics for a specific QR code.

        Args:
            qr_code_id: ID of the QR code
            days: Number of days to include in analysis

        Returns:
            dict: Analytics data
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Total scans
        total_scans = QRScan.query.filter_by(qr_code_id=qr_code_id).count()

        # Scans in period
        period_scans = QRScan.query.filter(
            QRScan.qr_code_id == qr_code_id,
            QRScan.scan_timestamp >= cutoff_date
        ).count()

        # Unique scans
        unique_scans = QRScan.query.filter(
            QRScan.qr_code_id == qr_code_id,
            QRScan.is_unique == True
        ).count()

        # Device breakdown
        device_stats = db.session.query(
            QRScan.device_type,
            func.count(QRScan.id).label('count')
        ).filter(
            QRScan.qr_code_id == qr_code_id,
            QRScan.scan_timestamp >= cutoff_date
        ).group_by(QRScan.device_type).all()

        # Browser breakdown
        browser_stats = db.session.query(
            QRScan.browser,
            func.count(QRScan.id).label('count')
        ).filter(
            QRScan.qr_code_id == qr_code_id,
            QRScan.scan_timestamp >= cutoff_date
        ).group_by(QRScan.browser).limit(10).all()

        # OS breakdown
        os_stats = db.session.query(
            QRScan.operating_system,
            func.count(QRScan.id).label('count')
        ).filter(
            QRScan.qr_code_id == qr_code_id,
            QRScan.scan_timestamp >= cutoff_date
        ).group_by(QRScan.operating_system).all()

        # Country breakdown
        country_stats = db.session.query(
            QRScan.country,
            func.count(QRScan.id).label('count')
        ).filter(
            QRScan.qr_code_id == qr_code_id,
            QRScan.scan_timestamp >= cutoff_date,
            QRScan.country.isnot(None)
        ).group_by(QRScan.country).limit(10).all()

        # Scans over time (daily)
        scans_over_time = db.session.query(
            func.date(QRScan.scan_timestamp).label('date'),
            func.count(QRScan.id).label('count')
        ).filter(
            QRScan.qr_code_id == qr_code_id,
            QRScan.scan_timestamp >= cutoff_date
        ).group_by(func.date(QRScan.scan_timestamp)).order_by('date').all()

        return {
            'total_scans': total_scans,
            'period_scans': period_scans,
            'unique_scans': unique_scans,
            'repeat_scans': total_scans - unique_scans,
            'devices': {row.device_type: row.count for row in device_stats},
            'browsers': {row.browser: row.count for row in browser_stats},
            'operating_systems': {row.operating_system: row.count for row in os_stats},
            'countries': {row.country: row.count for row in country_stats},
            'scans_over_time': [
                {'date': str(row.date), 'count': row.count}
                for row in scans_over_time
            ]
        }

    @staticmethod
    def get_brand_analytics(brand_id, days=30):
        """Get analytics for all QR codes in a brand."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Get all QR codes for this brand
        from models import QRCode
        qr_codes = QRCode.query.filter_by(brand_id=brand_id).all()
        qr_code_ids = [qr.id for qr in qr_codes]

        if not qr_code_ids:
            return {'total_scans': 0, 'unique_scans': 0}

        # Total scans for brand
        total_scans = QRScan.query.filter(
            QRScan.qr_code_id.in_(qr_code_ids)
        ).count()

        # Period scans
        period_scans = QRScan.query.filter(
            QRScan.qr_code_id.in_(qr_code_ids),
            QRScan.scan_timestamp >= cutoff_date
        ).count()

        # Unique scans
        unique_scans = QRScan.query.filter(
            QRScan.qr_code_id.in_(qr_code_ids),
            QRScan.is_unique == True
        ).count()

        # Top performing QR codes
        top_qr_codes = db.session.query(
            QRCode.id,
            QRCode.name,
            func.count(QRScan.id).label('scan_count')
        ).join(
            QRScan, QRCode.id == QRScan.qr_code_id
        ).filter(
            QRCode.brand_id == brand_id,
            QRScan.scan_timestamp >= cutoff_date
        ).group_by(QRCode.id, QRCode.name).order_by(
            func.count(QRScan.id).desc()
        ).limit(10).all()

        return {
            'total_scans': total_scans,
            'period_scans': period_scans,
            'unique_scans': unique_scans,
            'repeat_scans': total_scans - unique_scans,
            'total_qr_codes': len(qr_codes),
            'top_qr_codes': [
                {'id': row.id, 'name': row.name, 'scans': row.scan_count}
                for row in top_qr_codes
            ]
        }

    @staticmethod
    def get_employee_analytics(employee_id, days=30):
        """Get analytics for an employee's vCard QR codes."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Get employee's QR codes (via vCard profile)
        from models import Employee, VCardProfile, QRCode

        employee = Employee.query.get(employee_id)
        if not employee or not employee.vcard_profile:
            return {'total_scans': 0}

        qr_code_id = employee.vcard_profile.qr_code_id
        if not qr_code_id:
            return {'total_scans': 0}

        # Use existing get_qr_analytics
        return AnalyticsService.get_qr_analytics(qr_code_id, days)
