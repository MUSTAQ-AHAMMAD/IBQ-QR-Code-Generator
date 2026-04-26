#!/usr/bin/env python3
"""
Screenshot capture script for IBQ QR Code Generator application.
Captures all functionalities and saves them in organized directories.
"""
import asyncio
import os
from playwright.async_api import async_playwright

BASE_URL = "http://127.0.0.1:5000"
SCREENSHOTS_DIR = "/home/runner/work/IBQ-QR-Code-Generator/IBQ-QR-Code-Generator/screenshots"

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

async def setup_browser(playwright):
    """Launch browser and return page object."""
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = await context.new_page()
    return browser, page

async def login(page):
    """Login to the application."""
    print("Logging in...")
    await page.goto(f"{BASE_URL}/login")
    await page.wait_for_load_state('networkidle')
    await page.fill('input[name="username"]', ADMIN_USERNAME)
    await page.fill('input[name="password"]', ADMIN_PASSWORD)
    await page.click('input[type="submit"]')
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    print("Logged in successfully")

async def capture_authentication_pages(page):
    """Capture authentication related pages."""
    print("\n=== Capturing Authentication Pages ===")

    # Login page
    print("Capturing login page...")
    await page.goto(f"{BASE_URL}/login")
    await page.wait_for_load_state('networkidle')
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/01-authentication/01-login-page.png", full_page=True)

    # Registration page
    print("Capturing registration page...")
    await page.goto(f"{BASE_URL}/register")
    await page.wait_for_load_state('networkidle')
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/01-authentication/02-registration-page.png", full_page=True)

    print("Authentication pages captured ✓")

async def capture_dashboard_pages(page):
    """Capture dashboard and home pages."""
    print("\n=== Capturing Dashboard Pages ===")

    # Login first
    await login(page)

    # Dashboard home - light theme
    print("Capturing dashboard home (light theme)...")
    await page.goto(f"{BASE_URL}/dashboard")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/02-dashboard/01-dashboard-home-light.png", full_page=True)

    # Toggle to dark theme
    print("Capturing dashboard home (dark theme)...")
    await page.click('#themeToggle')
    await asyncio.sleep(1)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/02-dashboard/02-dashboard-home-dark.png", full_page=True)

    # Toggle back to light theme
    await page.click('#themeToggle')
    await asyncio.sleep(1)

    print("Dashboard pages captured ✓")

async def capture_qr_generation_pages(page):
    """Capture QR code generation for all 16 types."""
    print("\n=== Capturing QR Generation Pages ===")

    # Navigate to generation page
    await page.goto(f"{BASE_URL}/generate")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(3)

    # Wait for qrType select element to be available
    await page.wait_for_selector('#qrType', state='visible')

    qr_types = [
        ("vcard", "01-generate-business-card"),
        ("url", "02-generate-url"),
        ("text", "03-generate-text"),
        ("email", "04-generate-email"),
        ("sms", "05-generate-sms"),
        ("phone", "06-generate-phone"),
        ("wifi", "07-generate-wifi"),
        ("facebook", "08-generate-facebook"),
        ("twitter", "09-generate-twitter"),
        ("instagram", "10-generate-instagram"),
        ("linkedin", "11-generate-linkedin"),
        ("youtube", "12-generate-youtube"),
        ("app_store", "13-generate-appstore"),
        ("google_play", "14-generate-playstore"),
        ("event", "15-generate-calendar"),
        ("location", "16-generate-location"),
    ]

    for qr_type, filename in qr_types:
        print(f"Capturing QR generation form: {qr_type}...")
        await page.select_option('#qrType', qr_type)
        await asyncio.sleep(1.5)
        await page.screenshot(path=f"{SCREENSHOTS_DIR}/03-qr-generation/{filename}.png", full_page=True)

    print("QR generation pages captured ✓")

async def generate_sample_qr_codes(page):
    """Generate some sample QR codes for testing."""
    print("\n=== Generating Sample QR Codes ===")

    # Generate a URL QR code
    print("Generating URL QR code...")
    await page.goto(f"{BASE_URL}/generate")
    await page.wait_for_load_state('networkidle')
    await page.select_option('#qrType', 'url')
    await asyncio.sleep(1)
    await page.fill('input[name="name"]', 'GitHub Repository')
    await page.fill('input[name="url"]', 'https://github.com/MUSTAQ-AHAMMAD/IBQ-QR-Code-Generator')
    await page.click('input[type="submit"]')
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)

    # Generate a text QR code
    print("Generating Text QR code...")
    await page.goto(f"{BASE_URL}/generate")
    await page.wait_for_load_state('networkidle')
    await page.select_option('#qrType', 'text')
    await asyncio.sleep(1)
    await page.fill('input[name="name"]', 'Welcome Message')
    await page.fill('textarea[name="text_content"]', 'Welcome to IBQ QR Code Generator!')
    await page.click('input[type="submit"]')
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)

    # Generate an email QR code
    print("Generating Email QR code...")
    await page.goto(f"{BASE_URL}/generate")
    await page.wait_for_load_state('networkidle')
    await page.select_option('#qrType', 'email')
    await asyncio.sleep(1)
    await page.fill('input[name="name"]', 'Contact Support')
    await page.fill('input[name="email_address"]', 'support@example.com')
    await page.fill('input[name="email_subject"]', 'Support Request')
    await page.click('input[type="submit"]')
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)

    print("Sample QR codes generated ✓")

async def capture_qr_management_pages(page):
    """Capture QR code management pages."""
    print("\n=== Capturing QR Management Pages ===")

    # My QR Codes list
    print("Capturing My QR Codes page...")
    await page.goto(f"{BASE_URL}/my-qrcodes")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/04-qr-management/01-my-qrcodes-list.png", full_page=True)

    # Try to view a QR code if any exist
    try:
        view_button = page.locator('a:has-text("View")').first
        if await view_button.count() > 0:
            print("Capturing View QR Code page...")
            await view_button.click()
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            await page.screenshot(path=f"{SCREENSHOTS_DIR}/04-qr-management/02-view-qrcode.png", full_page=True)

            # Go back and try edit
            await page.goto(f"{BASE_URL}/my-qrcodes")
            await page.wait_for_load_state('networkidle')
            edit_button = page.locator('a:has-text("Edit")').first
            if await edit_button.count() > 0:
                print("Capturing Edit QR Code page...")
                await edit_button.click()
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)
                await page.screenshot(path=f"{SCREENSHOTS_DIR}/04-qr-management/03-edit-qrcode.png", full_page=True)
    except Exception as e:
        print(f"Note: Could not capture view/edit pages: {e}")

    print("QR management pages captured ✓")

async def capture_template_pages(page):
    """Capture template management pages."""
    print("\n=== Capturing Template Pages ===")

    # Templates list
    print("Capturing Templates page...")
    await page.goto(f"{BASE_URL}/templates")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/05-templates/01-templates-list.png", full_page=True)

    # Create template page
    print("Capturing Create Template page...")
    await page.goto(f"{BASE_URL}/templates/create")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/05-templates/02-create-template.png", full_page=True)

    print("Template pages captured ✓")

async def capture_settings_pages(page):
    """Capture settings pages."""
    print("\n=== Capturing Settings Pages ===")

    # Profile settings
    print("Capturing Profile Settings page...")
    await page.goto(f"{BASE_URL}/settings/profile")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/06-settings/01-profile-settings.png", full_page=True)

    # Password settings
    print("Capturing Change Password page...")
    await page.goto(f"{BASE_URL}/settings/password")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/06-settings/02-change-password.png", full_page=True)

    # Account settings
    print("Capturing Account Settings page...")
    await page.goto(f"{BASE_URL}/settings/account")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/06-settings/03-account-settings.png", full_page=True)

    # API Key settings
    print("Capturing API Key page...")
    await page.goto(f"{BASE_URL}/settings/api-key")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/06-settings/04-api-key.png", full_page=True)

    print("Settings pages captured ✓")

async def capture_help_pages(page):
    """Capture help and support pages."""
    print("\n=== Capturing Help Pages ===")

    # Documentation
    print("Capturing Documentation page...")
    await page.goto(f"{BASE_URL}/help/documentation")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/07-help/01-documentation.png", full_page=True)

    # FAQ
    print("Capturing FAQ page...")
    await page.goto(f"{BASE_URL}/help/faq")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/07-help/02-faq.png", full_page=True)

    # Contact
    print("Capturing Contact page...")
    await page.goto(f"{BASE_URL}/help/contact")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/07-help/03-contact.png", full_page=True)

    # Help
    print("Capturing Help page...")
    await page.goto(f"{BASE_URL}/help")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)
    await page.screenshot(path=f"{SCREENSHOTS_DIR}/07-help/04-help.png", full_page=True)

    print("Help pages captured ✓")

async def main():
    """Main function to capture all screenshots."""
    print("=" * 60)
    print("IBQ QR Code Generator - Screenshot Capture Script")
    print("=" * 60)

    async with async_playwright() as playwright:
        browser, page = await setup_browser(playwright)

        try:
            # Capture authentication pages (before login)
            await capture_authentication_pages(page)

            # Capture dashboard pages (after login)
            await capture_dashboard_pages(page)

            # Capture QR generation pages
            await capture_qr_generation_pages(page)

            # Generate some sample QR codes
            await generate_sample_qr_codes(page)

            # Capture QR management pages
            await capture_qr_management_pages(page)

            # Capture template pages
            await capture_template_pages(page)

            # Capture settings pages
            await capture_settings_pages(page)

            # Capture help pages
            await capture_help_pages(page)

            print("\n" + "=" * 60)
            print("✓ All screenshots captured successfully!")
            print(f"Screenshots saved in: {SCREENSHOTS_DIR}")
            print("=" * 60)

        except Exception as e:
            print(f"\n✗ Error occurred: {e}")
            import traceback
            traceback.print_exc()

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
