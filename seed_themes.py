"""
Seed theme presets for the application.
Creates 6 professional theme presets: Corporate, Modern, Luxury, Minimal, Tech, Creative
"""
from app import create_app
from models import db, Theme

def seed_themes():
    """Seed the database with default theme presets."""
    app = create_app()

    with app.app_context():
        print("Seeding theme presets...")

        # Check if themes already exist
        if Theme.query.count() > 0:
            print("Themes already exist. Skipping seed.")
            return

        themes_data = [
            {
                "name": "Corporate",
                "slug": "corporate",
                "description": "Professional corporate theme with clean lines and business-focused colors",
                "category": "preset",
                "theme_config": {
                    "colors": {
                        "primary": "#0047AB",
                        "secondary": "#002366",
                        "background": "#FFFFFF",
                        "text": "#333333",
                        "accent": "#4A90E2"
                    },
                    "typography": {
                        "fontFamily": "Inter, sans-serif",
                        "headingWeight": "600",
                        "bodyWeight": "400"
                    },
                    "buttons": {
                        "style": "square",
                        "shadow": True,
                        "radius": "4px"
                    },
                    "cards": {
                        "style": "shadow",
                        "radius": "8px",
                        "shadow": "0 2px 8px rgba(0,0,0,0.1)"
                    },
                    "qr": {
                        "style": "square",
                        "eyeStyle": "square",
                        "dataStyle": "square"
                    }
                },
                "is_public": True,
                "is_default": True
            },
            {
                "name": "Modern",
                "slug": "modern",
                "description": "Contemporary theme with vibrant gradients and rounded elements",
                "category": "preset",
                "theme_config": {
                    "colors": {
                        "primary": "#667eea",
                        "secondary": "#764ba2",
                        "background": "#F7FAFC",
                        "text": "#2D3748",
                        "accent": "#F687B3"
                    },
                    "typography": {
                        "fontFamily": "Poppins, sans-serif",
                        "headingWeight": "600",
                        "bodyWeight": "400"
                    },
                    "buttons": {
                        "style": "rounded",
                        "shadow": True,
                        "radius": "12px"
                    },
                    "cards": {
                        "style": "shadow",
                        "radius": "16px",
                        "shadow": "0 4px 12px rgba(102,126,234,0.15)"
                    },
                    "qr": {
                        "style": "rounded",
                        "eyeStyle": "rounded",
                        "dataStyle": "rounded"
                    }
                },
                "is_public": True
            },
            {
                "name": "Luxury",
                "slug": "luxury",
                "description": "Elegant luxury theme with gold accents and premium feel",
                "category": "preset",
                "theme_config": {
                    "colors": {
                        "primary": "#1a1a1a",
                        "secondary": "#C9A961",
                        "background": "#FAFAFA",
                        "text": "#2C2C2C",
                        "accent": "#D4AF37"
                    },
                    "typography": {
                        "fontFamily": "Playfair Display, serif",
                        "headingWeight": "700",
                        "bodyWeight": "400"
                    },
                    "buttons": {
                        "style": "square",
                        "shadow": False,
                        "radius": "2px"
                    },
                    "cards": {
                        "style": "border",
                        "radius": "4px",
                        "border": "1px solid #C9A961"
                    },
                    "qr": {
                        "style": "square",
                        "eyeStyle": "square",
                        "dataStyle": "square"
                    }
                },
                "is_public": True
            },
            {
                "name": "Minimal",
                "slug": "minimal",
                "description": "Clean minimal theme with focus on content and simplicity",
                "category": "preset",
                "theme_config": {
                    "colors": {
                        "primary": "#000000",
                        "secondary": "#666666",
                        "background": "#FFFFFF",
                        "text": "#1A1A1A",
                        "accent": "#E0E0E0"
                    },
                    "typography": {
                        "fontFamily": "Helvetica Neue, sans-serif",
                        "headingWeight": "500",
                        "bodyWeight": "300"
                    },
                    "buttons": {
                        "style": "square",
                        "shadow": False,
                        "radius": "0px"
                    },
                    "cards": {
                        "style": "flat",
                        "radius": "0px",
                        "border": "none"
                    },
                    "qr": {
                        "style": "square",
                        "eyeStyle": "square",
                        "dataStyle": "square"
                    }
                },
                "is_public": True
            },
            {
                "name": "Tech",
                "slug": "tech",
                "description": "Tech-focused theme with blue gradients and futuristic feel",
                "category": "preset",
                "theme_config": {
                    "colors": {
                        "primary": "#00D9FF",
                        "secondary": "#0099CC",
                        "background": "#0A192F",
                        "text": "#E6F1FF",
                        "accent": "#64FFDA"
                    },
                    "typography": {
                        "fontFamily": "Roboto Mono, monospace",
                        "headingWeight": "600",
                        "bodyWeight": "400"
                    },
                    "buttons": {
                        "style": "rounded",
                        "shadow": True,
                        "radius": "8px"
                    },
                    "cards": {
                        "style": "shadow",
                        "radius": "12px",
                        "shadow": "0 4px 20px rgba(0,217,255,0.2)"
                    },
                    "qr": {
                        "style": "dots",
                        "eyeStyle": "rounded",
                        "dataStyle": "dot"
                    }
                },
                "is_public": True
            },
            {
                "name": "Creative",
                "slug": "creative",
                "description": "Bold creative theme with vibrant colors and playful elements",
                "category": "preset",
                "theme_config": {
                    "colors": {
                        "primary": "#FF6B6B",
                        "secondary": "#4ECDC4",
                        "background": "#FFF9F5",
                        "text": "#2C2C2C",
                        "accent": "#FFE66D"
                    },
                    "typography": {
                        "fontFamily": "Quicksand, sans-serif",
                        "headingWeight": "700",
                        "bodyWeight": "500"
                    },
                    "buttons": {
                        "style": "pill",
                        "shadow": True,
                        "radius": "50px"
                    },
                    "cards": {
                        "style": "shadow",
                        "radius": "20px",
                        "shadow": "0 8px 16px rgba(255,107,107,0.15)"
                    },
                    "qr": {
                        "style": "dots",
                        "eyeStyle": "circle",
                        "dataStyle": "dot"
                    }
                },
                "is_public": True
            }
        ]

        for theme_data in themes_data:
            theme = Theme(**theme_data)
            db.session.add(theme)

        try:
            db.session.commit()
            print(f"✅ Successfully created {len(themes_data)} theme presets!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating themes: {e}")

if __name__ == '__main__':
    seed_themes()
