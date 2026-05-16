"""
Production middleware and utilities.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import request, jsonify
from functools import wraps


def setup_logging(app):
    """Configure application logging for production."""
    if not app.debug:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # File handler with rotation
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=app.config['LOG_MAX_BYTES'],
            backupCount=app.config['LOG_BACKUP_COUNT']
        )

        # Set format
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))

        # Add handler to app logger
        app.logger.addHandler(file_handler)
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.info('IBQ QR Code Generator startup')


def setup_sentry(app):
    """Initialize Sentry error tracking."""
    if app.config.get('SENTRY_DSN'):
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration

            sentry_sdk.init(
                dsn=app.config['SENTRY_DSN'],
                integrations=[FlaskIntegration()],
                traces_sample_rate=app.config['SENTRY_TRACES_SAMPLE_RATE'],
                environment=app.config['SENTRY_ENVIRONMENT']
            )
            app.logger.info('Sentry error tracking initialized')
        except ImportError:
            app.logger.warning('Sentry SDK not installed, skipping error tracking')


def setup_security_headers(app):
    """Add security headers to all responses."""
    @app.after_request
    def set_security_headers(response):
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'

        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'

        # XSS Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Strict Transport Security (only if HTTPS)
        if request.is_secure:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
            "img-src 'self' data: blob:; "
            "font-src 'self' cdn.jsdelivr.net; "
            "connect-src 'self';"
        )

        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions Policy
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

        return response


def setup_rate_limiting(app):
    """Configure rate limiting."""
    if app.config.get('RATELIMIT_ENABLED'):
        try:
            from flask_limiter import Limiter
            from flask_limiter.util import get_remote_address

            limiter = Limiter(
                app=app,
                key_func=get_remote_address,
                default_limits=[app.config['RATELIMIT_DEFAULT']],
                storage_uri=app.config['RATELIMIT_STORAGE_URL']
            )

            app.logger.info('Rate limiting enabled')
            return limiter
        except ImportError:
            app.logger.warning('Flask-Limiter not installed, rate limiting disabled')
            return None
    return None


def setup_caching(app):
    """Configure caching."""
    try:
        from flask_caching import Cache

        cache = Cache(app)
        app.logger.info(f"Caching initialized with {app.config['CACHE_TYPE']}")
        return cache
    except ImportError:
        app.logger.warning('Flask-Caching not installed, caching disabled')
        return None


def health_check_route(app, db):
    """Add health check endpoint."""
    @app.route('/health')
    def health_check():
        """Health check endpoint for load balancers and monitoring."""
        try:
            # Check database connection
            db.session.execute('SELECT 1')

            return jsonify({
                'status': 'healthy',
                'app': app.config['APP_NAME'],
                'version': app.config['APP_VERSION'],
                'database': 'connected'
            }), 200
        except Exception as e:
            app.logger.error(f'Health check failed: {str(e)}')
            return jsonify({
                'status': 'unhealthy',
                'error': 'Database connection failed'
            }), 503


def readiness_check_route(app, db):
    """Add readiness check endpoint."""
    @app.route('/ready')
    def readiness_check():
        """Readiness check endpoint for Kubernetes."""
        try:
            # Check database
            db.session.execute('SELECT 1')

            # Check upload folder exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                return jsonify({'status': 'not ready', 'error': 'Upload folder missing'}), 503

            return jsonify({
                'status': 'ready',
                'checks': {
                    'database': 'ok',
                    'filesystem': 'ok'
                }
            }), 200
        except Exception as e:
            app.logger.error(f'Readiness check failed: {str(e)}')
            return jsonify({
                'status': 'not ready',
                'error': str(e)
            }), 503


def metrics_route(app, db):
    """Add basic metrics endpoint."""
    from models import User, QRCode
    from flask_login import login_required

    @app.route('/metrics')
    @login_required
    def metrics():
        """Basic application metrics."""
        try:
            total_users = User.query.count()
            total_qrcodes = QRCode.query.count()

            return jsonify({
                'total_users': total_users,
                'total_qrcodes': total_qrcodes,
                'app_version': app.config['APP_VERSION']
            }), 200
        except Exception as e:
            app.logger.error(f'Metrics retrieval failed: {str(e)}')
            return jsonify({'error': 'Failed to retrieve metrics'}), 500


def request_id_middleware(app):
    """Add request ID to all requests for tracing."""
    import uuid

    @app.before_request
    def add_request_id():
        request.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))

    @app.after_request
    def add_request_id_header(response):
        if hasattr(request, 'request_id'):
            response.headers['X-Request-ID'] = request.request_id
        return response
