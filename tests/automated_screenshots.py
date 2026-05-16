#!/usr/bin/env python3
"""
Comprehensive automated screenshot capture system for IBQ QR Code Generator.
Captures screenshots across all viewports, themes, and pages.
"""
import asyncio
import os
from playwright.async_api import async_playwright
from datetime import datetime

BASE_URL = os.getenv("TEST_BASE_URL", "http://127.0.0.1:5000")
SCREENSHOTS_DIR = "/home/runner/work/IBQ-QR-Code-Generator/IBQ-QR-Code-Generator/qa-reports/screenshots"

# Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Viewports
VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "laptop": {"width": 1366, "height": 768},
    "tablet": {"width": 768, "height": 1024},
    "ipad": {"width": 1024, "height": 1366},
    "mobile": {"width": 375, "height": 812},
    "android": {"width": 412, "height": 915},
}

# Pages to capture
PAGES_TO_CAPTURE = {
    "public": [
        ("/", "homepage"),
        ("/login", "login"),
        ("/register", "register"),
    ],
    "authenticated": [
        ("/dashboard", "dashboard"),
        ("/generate", "qr_generate"),
        ("/my-qrcodes", "my_qrcodes"),
        ("/brands", "brands"),
        ("/brands/create", "create_brand"),
        ("/templates", "templates"),
        ("/templates/create", "create_template"),
        ("/settings/profile", "settings_profile"),
        ("/settings/password", "settings_password"),
        ("/settings/account", "settings_account"),
        ("/settings/api-key", "settings_api"),
        ("/help", "help"),
        ("/help/documentation", "documentation"),
        ("/help/faq", "faq"),
        ("/help/contact", "contact"),
    ],
}

# QR types for form screenshots
QR_TYPES = [
    ("vcard", "business_card"),
    ("url", "url"),
    ("text", "text"),
    ("email", "email"),
    ("sms", "sms"),
    ("phone", "phone"),
    ("wifi", "wifi"),
    ("facebook", "facebook"),
    ("twitter", "twitter"),
    ("instagram", "instagram"),
    ("linkedin", "linkedin"),
    ("youtube", "youtube"),
    ("app_store", "app_store"),
    ("google_play", "google_play"),
    ("event", "calendar_event"),
    ("location", "location"),
]


async def setup_browser(playwright, viewport):
    """Launch browser with specific viewport."""
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(viewport=viewport)
    page = await context.new_page()
    return browser, page


async def login(page):
    """Login to the application."""
    print("  Logging in...")
    await page.goto(f"{BASE_URL}/login")
    await page.wait_for_load_state('networkidle')
    await page.fill('input[name="username"]', ADMIN_USERNAME)
    await page.fill('input[name="password"]', ADMIN_PASSWORD)
    await page.click('input[type="submit"]')
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)


async def capture_public_pages(page, viewport_name):
    """Capture public pages."""
    print(f"\n=== Capturing Public Pages ({viewport_name}) ===")

    for url, name in PAGES_TO_CAPTURE["public"]:
        try:
            print(f"  Capturing {name}...")
            await page.goto(f"{BASE_URL}{url}")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)

            screenshot_path = os.path.join(SCREENSHOTS_DIR, viewport_name, f"{name}.png")
            await page.screenshot(path=screenshot_path, full_page=True)
        except Exception as e:
            print(f"  Error capturing {name}: {e}")


async def capture_authenticated_pages(page, viewport_name, theme="light"):
    """Capture authenticated pages."""
    print(f"\n=== Capturing Authenticated Pages ({viewport_name}, {theme} mode) ===")

    # Login first
    await login(page)

    # Set theme if dark mode
    if theme == "dark":
        try:
            await page.goto(f"{BASE_URL}/dashboard")
            await page.wait_for_load_state('networkidle')
            theme_toggle = page.locator('#themeToggle, .theme-toggle').first
            if await theme_toggle.count() > 0:
                await theme_toggle.click()
                await asyncio.sleep(1)
        except Exception as e:
            print(f"  Could not toggle theme: {e}")

    for url, name in PAGES_TO_CAPTURE["authenticated"]:
        try:
            print(f"  Capturing {name}...")
            await page.goto(f"{BASE_URL}{url}")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)

            theme_dir = os.path.join(SCREENSHOTS_DIR, f"{theme}-mode", viewport_name)
            os.makedirs(theme_dir, exist_ok=True)
            screenshot_path = os.path.join(theme_dir, f"{name}.png")
            await page.screenshot(path=screenshot_path, full_page=True)
        except Exception as e:
            print(f"  Error capturing {name}: {e}")


async def capture_qr_forms(page, viewport_name):
    """Capture all QR type forms."""
    print(f"\n=== Capturing QR Forms ({viewport_name}) ===")

    await page.goto(f"{BASE_URL}/generate")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)

    for qr_type, name in QR_TYPES:
        try:
            print(f"  Capturing QR form: {name}...")
            await page.select_option('#qrType, select[name="qr_type"]', qr_type)
            await asyncio.sleep(1.5)

            screenshot_path = os.path.join(SCREENSHOTS_DIR, "qr-forms", viewport_name, f"{name}.png")
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            await page.screenshot(path=screenshot_path, full_page=True)
        except Exception as e:
            print(f"  Error capturing {name}: {e}")


async def capture_viewport(playwright, viewport_name, viewport_size):
    """Capture all screenshots for a specific viewport."""
    print(f"\n{'='*60}")
    print(f"CAPTURING VIEWPORT: {viewport_name} ({viewport_size['width']}x{viewport_size['height']})")
    print(f"{'='*60}")

    browser, page = await setup_browser(playwright, viewport_size)

    try:
        # Create viewport directory
        os.makedirs(os.path.join(SCREENSHOTS_DIR, viewport_name), exist_ok=True)

        # Capture public pages
        await capture_public_pages(page, viewport_name)

        # Capture authenticated pages (light mode)
        await capture_authenticated_pages(page, viewport_name, theme="light")

        # Capture authenticated pages (dark mode)
        await capture_authenticated_pages(page, viewport_name, theme="dark")

        # Capture QR forms (only for desktop and mobile)
        if viewport_name in ["desktop", "mobile"]:
            await login(page)
            await capture_qr_forms(page, viewport_name)

    finally:
        await browser.close()


async def main():
    """Main function to capture all screenshots."""
    print("=" * 60)
    print("IBQ QR Code Generator - Comprehensive Screenshot Capture")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"Screenshots Directory: {SCREENSHOTS_DIR}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    # Create base directories
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(os.path.join(SCREENSHOTS_DIR, "light-mode"), exist_ok=True)
    os.makedirs(os.path.join(SCREENSHOTS_DIR, "dark-mode"), exist_ok=True)
    os.makedirs(os.path.join(SCREENSHOTS_DIR, "qr-forms"), exist_ok=True)

    async with async_playwright() as playwright:
        # Capture screenshots for each viewport
        for viewport_name, viewport_size in VIEWPORTS.items():
            try:
                await capture_viewport(playwright, viewport_name, viewport_size)
            except Exception as e:
                print(f"\nError with viewport {viewport_name}: {e}")
                import traceback
                traceback.print_exc()

    print("\n" + "=" * 60)
    print("✓ Screenshot capture completed!")
    print(f"Screenshots saved in: {SCREENSHOTS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
