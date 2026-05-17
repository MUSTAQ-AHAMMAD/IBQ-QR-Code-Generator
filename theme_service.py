"""
Theme service for dynamic brand theming.
Handles CSS variable injection, theme switching, and brand-based theming.
"""
from flask import request, session
from models import Brand, Theme, Organization
import re

class ThemeService:
    """Service for managing dynamic themes and brand styling."""

    @staticmethod
    def get_brand_from_request():
        """
        Detect brand from various sources:
        1. Query parameter (?brand=slug)
        2. Subdomain (brand.app.com)
        3. Custom domain (brand.com)
        4. Session storage
        5. Default brand for user
        """
        # Check query parameter
        brand_slug = request.args.get('brand')
        if brand_slug:
            brand = Brand.query.filter_by(slug=brand_slug, is_active=True).first()
            if brand:
                session['brand_id'] = brand.id
                return brand

        # Check subdomain
        host = request.host.lower()
        subdomain = host.split('.')[0] if '.' in host else None

        if subdomain and subdomain not in ['www', 'app', 'api']:
            # Try to find organization by subdomain
            org = Organization.query.filter_by(subdomain=subdomain, is_active=True).first()
            if org and org.brands.first():
                brand = org.brands.filter_by(is_default=True).first() or org.brands.first()
                session['brand_id'] = brand.id
                return brand

            # Try to find brand by subdomain (legacy)
            brand = Brand.query.filter_by(slug=subdomain, is_active=True).first()
            if brand:
                session['brand_id'] = brand.id
                return brand

        # Check custom domain
        org = Organization.query.filter_by(domain=host, is_active=True).first()
        if org and org.brands.first():
            brand = org.brands.filter_by(is_default=True).first() or org.brands.first()
            session['brand_id'] = brand.id
            return brand

        # Check session
        brand_id = session.get('brand_id')
        if brand_id:
            brand = Brand.query.get(brand_id)
            if brand and brand.is_active:
                return brand

        # Return None if no brand found
        return None

    @staticmethod
    def generate_css_variables(brand, theme=None):
        """
        Generate CSS custom properties from brand and theme configuration.

        Args:
            brand: Brand model instance
            theme: Optional Theme model instance

        Returns:
            str: CSS custom properties as string
        """
        if not brand:
            return ""

        # Start with brand colors
        css_vars = {
            '--brand-primary': brand.primary_color or '#667eea',
            '--brand-secondary': brand.secondary_color or '#764ba2',
            '--brand-background': brand.background_color or '#ffffff',
            '--brand-font-family': brand.font_family or 'Inter, sans-serif',
        }

        # Apply theme configuration if provided
        if theme and theme.theme_config:
            config = theme.theme_config

            if 'colors' in config:
                css_vars.update({
                    '--theme-primary': config['colors'].get('primary', brand.primary_color),
                    '--theme-secondary': config['colors'].get('secondary', brand.secondary_color),
                    '--theme-background': config['colors'].get('background', '#ffffff'),
                    '--theme-text': config['colors'].get('text', '#333333'),
                    '--theme-accent': config['colors'].get('accent', brand.primary_color),
                })

            if 'typography' in config:
                css_vars.update({
                    '--theme-font-family': config['typography'].get('fontFamily', brand.font_family),
                    '--theme-heading-weight': config['typography'].get('headingWeight', '600'),
                    '--theme-body-weight': config['typography'].get('bodyWeight', '400'),
                })

            if 'buttons' in config:
                css_vars.update({
                    '--button-radius': config['buttons'].get('radius', '8px'),
                })

            if 'cards' in config:
                css_vars.update({
                    '--card-radius': config['cards'].get('radius', '12px'),
                    '--card-shadow': config['cards'].get('shadow', '0 2px 8px rgba(0,0,0,0.1)'),
                })

        # Generate CSS string
        css_lines = [':root {']
        for key, value in css_vars.items():
            css_lines.append(f'  {key}: {value};')
        css_lines.append('}')

        return '\n'.join(css_lines)

    @staticmethod
    def generate_theme_json(brand, theme=None):
        """
        Generate theme configuration as JSON for JavaScript consumption.

        Args:
            brand: Brand model instance
            theme: Optional Theme model instance

        Returns:
            dict: Theme configuration
        """
        if not brand:
            return {}

        theme_data = {
            'brand': {
                'id': brand.id,
                'name': brand.name,
                'slug': brand.slug,
                'logo': brand.logo,
                'favicon': brand.favicon,
                'primaryColor': brand.primary_color,
                'secondaryColor': brand.secondary_color,
                'backgroundColor': brand.background_color,
                'fontFamily': brand.font_family,
                'buttonStyle': brand.button_style,
                'cardStyle': brand.card_style,
                'qrStylePreset': brand.qr_style_preset,
            }
        }

        if theme and theme.theme_config:
            theme_data['preset'] = {
                'id': theme.id,
                'name': theme.name,
                'slug': theme.slug,
                'config': theme.theme_config
            }

        return theme_data

    @staticmethod
    def apply_employee_overrides(theme_data, employee):
        """
        Apply employee-specific branding overrides to theme.

        Args:
            theme_data: Base theme data dict
            employee: Employee model instance

        Returns:
            dict: Theme data with employee overrides applied
        """
        if not employee:
            return theme_data

        if employee.custom_primary_color:
            theme_data['brand']['primaryColor'] = employee.custom_primary_color

        if employee.custom_qr_style:
            theme_data['brand']['qrStylePreset'] = employee.custom_qr_style

        if employee.custom_landing_theme:
            theme_data['employee'] = {
                'customTheme': employee.custom_landing_theme
            }

        return theme_data

    @staticmethod
    def get_theme_preset_by_slug(slug):
        """Get theme preset by slug."""
        return Theme.query.filter_by(slug=slug, is_public=True).first()

    @staticmethod
    def get_all_theme_presets():
        """Get all public theme presets."""
        return Theme.query.filter_by(is_public=True, category='preset').all()


def inject_brand_theme():
    """
    Flask context processor to inject brand theme into all templates.
    Add this to your Flask app:

    @app.context_processor
    def inject_brand_theme():
        from theme_service import inject_brand_theme
        return inject_brand_theme()
    """
    theme_service = ThemeService()
    brand = theme_service.get_brand_from_request()

    # Get theme preset if brand has one
    theme = None
    if brand and brand.qr_style_preset:
        theme = theme_service.get_theme_preset_by_slug(brand.qr_style_preset)

    return {
        'current_brand': brand,
        'current_theme': theme,
        'brand_css': theme_service.generate_css_variables(brand, theme),
        'brand_theme_json': theme_service.generate_theme_json(brand, theme)
    }
