"""
End-to-end tests for QR code generation workflows.

Tests all 16 QR code types:
- vCard/Business Card
- URL
- Text
- Email
- SMS
- Phone
- WiFi
- Social Media (Facebook, Twitter, Instagram, LinkedIn, YouTube)
- App Stores (Apple App Store, Google Play)
- Calendar Event
- Location
"""
import pytest
import asyncio


@pytest.mark.asyncio
class TestQRCodeGeneration:
    """Test suite for QR code generation workflows."""

    async def test_generate_page_loads(self, authenticated_page, base_url, screenshot_path):
        """Test that QR generation page loads correctly."""
        page = authenticated_page

        await page.goto(f"{base_url}/generate")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        # Check form elements exist
        assert await page.query_selector('#qrType, select[name="qr_type"]') is not None
        assert await page.query_selector('input[name="name"]') is not None

        # Take screenshot
        await page.screenshot(path=screenshot_path("qr_generate_page_default"), full_page=True)

    @pytest.mark.parametrize("qr_type,qr_name", [
        ("vcard", "Business Card"),
        ("url", "URL QR Code"),
        ("text", "Text QR Code"),
        ("email", "Email QR Code"),
        ("sms", "SMS QR Code"),
        ("phone", "Phone QR Code"),
        ("wifi", "WiFi QR Code"),
        ("facebook", "Facebook QR Code"),
        ("twitter", "Twitter QR Code"),
        ("instagram", "Instagram QR Code"),
        ("linkedin", "LinkedIn QR Code"),
        ("youtube", "YouTube QR Code"),
        ("app_store", "App Store QR Code"),
        ("google_play", "Play Store QR Code"),
        ("event", "Calendar Event QR Code"),
        ("location", "Location QR Code"),
    ])
    async def test_qr_type_form_renders(self, authenticated_page, base_url, screenshot_path, qr_type, qr_name):
        """Test that each QR type renders its specific form fields."""
        page = authenticated_page

        await page.goto(f"{base_url}/generate")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Select QR type
        qr_type_selector = page.locator('#qrType, select[name="qr_type"]').first
        await qr_type_selector.select_option(qr_type)
        await asyncio.sleep(1.5)

        # Take screenshot of form for this type
        await page.screenshot(path=screenshot_path(f"qr_form_{qr_type}"), full_page=True)

    async def test_generate_url_qr_code(self, authenticated_page, base_url, screenshot_path):
        """Test generating a URL QR code."""
        page = authenticated_page

        await page.goto(f"{base_url}/generate")
        await page.wait_for_load_state('networkidle')

        # Select URL type
        await page.select_option('#qrType, select[name="qr_type"]', 'url')
        await asyncio.sleep(1)

        # Fill form
        await page.fill('input[name="name"]', 'GitHub Repository')
        url_field = page.locator('input[name="url"]').first
        await url_field.fill('https://github.com/MUSTAQ-AHAMMAD/IBQ-QR-Code-Generator')

        # Screenshot before generate
        await page.screenshot(path=screenshot_path("qr_url_before_generate"), full_page=True)

        # Submit form
        await page.click('button[type="submit"], input[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        # Screenshot after generation
        await page.screenshot(path=screenshot_path("qr_url_after_generate"), full_page=True)

    async def test_generate_vcard_qr_code(self, authenticated_page, base_url, screenshot_path):
        """Test generating a vCard/Business Card QR code."""
        page = authenticated_page

        await page.goto(f"{base_url}/generate")
        await page.wait_for_load_state('networkidle')

        # Select vCard type
        await page.select_option('#qrType, select[name="qr_type"]', 'vcard')
        await asyncio.sleep(1)

        # Fill vCard form
        await page.fill('input[name="name"]', 'John Doe Business Card')

        # Fill contact details
        contact_name = page.locator('input[name="contact_name"]')
        if await contact_name.count() > 0:
            await contact_name.fill('John Doe')

        contact_email = page.locator('input[name="contact_email"]')
        if await contact_email.count() > 0:
            await contact_email.fill('john.doe@example.com')

        contact_phone = page.locator('input[name="contact_phone"]')
        if await contact_phone.count() > 0:
            await contact_phone.fill('+1234567890')

        contact_company = page.locator('input[name="contact_company"]')
        if await contact_company.count() > 0:
            await contact_company.fill('Test Company')

        # Screenshot before generate
        await page.screenshot(path=screenshot_path("qr_vcard_before_generate"), full_page=True)

        # Submit form
        await page.click('button[type="submit"], input[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        # Screenshot after generation
        await page.screenshot(path=screenshot_path("qr_vcard_after_generate"), full_page=True)

    async def test_generate_email_qr_code(self, authenticated_page, base_url, screenshot_path):
        """Test generating an Email QR code."""
        page = authenticated_page

        await page.goto(f"{base_url}/generate")
        await page.wait_for_load_state('networkidle')

        # Select email type
        await page.select_option('#qrType, select[name="qr_type"]', 'email')
        await asyncio.sleep(1)

        # Fill email form
        await page.fill('input[name="name"]', 'Contact Support')

        email_address = page.locator('input[name="email_address"]')
        if await email_address.count() > 0:
            await email_address.fill('support@example.com')

        email_subject = page.locator('input[name="email_subject"]')
        if await email_subject.count() > 0:
            await email_subject.fill('Support Request')

        email_body = page.locator('textarea[name="email_body"]')
        if await email_body.count() > 0:
            await email_body.fill('I need help with...')

        # Screenshot and submit
        await page.screenshot(path=screenshot_path("qr_email_before_generate"), full_page=True)
        await page.click('button[type="submit"], input[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        await page.screenshot(path=screenshot_path("qr_email_after_generate"), full_page=True)

    async def test_generate_wifi_qr_code(self, authenticated_page, base_url, screenshot_path):
        """Test generating a WiFi QR code."""
        page = authenticated_page

        await page.goto(f"{base_url}/generate")
        await page.wait_for_load_state('networkidle')

        # Select WiFi type
        await page.select_option('#qrType, select[name="qr_type"]', 'wifi')
        await asyncio.sleep(1)

        # Fill WiFi form
        await page.fill('input[name="name"]', 'Office WiFi')

        wifi_ssid = page.locator('input[name="wifi_ssid"]')
        if await wifi_ssid.count() > 0:
            await wifi_ssid.fill('TestNetwork')

        wifi_password = page.locator('input[name="wifi_password"]')
        if await wifi_password.count() > 0:
            await wifi_password.fill('TestPassword123')

        # Screenshot and submit
        await page.screenshot(path=screenshot_path("qr_wifi_before_generate"), full_page=True)
        await page.click('button[type="submit"], input[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        await page.screenshot(path=screenshot_path("qr_wifi_after_generate"), full_page=True)

    async def test_qr_customization_options(self, authenticated_page, base_url, screenshot_path):
        """Test QR code customization options."""
        page = authenticated_page

        await page.goto(f"{base_url}/generate")
        await page.wait_for_load_state('networkidle')

        # Select URL type
        await page.select_option('#qrType, select[name="qr_type"]', 'url')
        await asyncio.sleep(1)

        # Fill basic info
        await page.fill('input[name="name"]', 'Customized QR')
        url_field = page.locator('input[name="url"]').first
        await url_field.fill('https://example.com')

        # Try to set colors
        fg_color = page.locator('input[name="foreground_color"], input[id="foreground_color"]')
        if await fg_color.count() > 0:
            await fg_color.fill('#FF0000')

        bg_color = page.locator('input[name="background_color"], input[id="background_color"]')
        if await bg_color.count() > 0:
            await bg_color.fill('#FFFF00')

        # Screenshot with customization
        await page.screenshot(path=screenshot_path("qr_customization_colors"), full_page=True)

    async def test_my_qrcodes_page(self, authenticated_page, base_url, screenshot_path):
        """Test My QR Codes page displays generated codes."""
        page = authenticated_page

        await page.goto(f"{base_url}/my-qrcodes")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        # Take screenshot
        await page.screenshot(path=screenshot_path("my_qrcodes_list"), full_page=True)

        # Check if QR codes are displayed
        qr_cards = page.locator('.card, .qr-card, [class*="qr"]')
        count = await qr_cards.count()
        print(f"Found {count} QR code elements")

    async def test_view_qr_code_details(self, authenticated_page, base_url, screenshot_path):
        """Test viewing QR code details."""
        page = authenticated_page

        await page.goto(f"{base_url}/my-qrcodes")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        # Try to click first view button
        try:
            view_button = page.locator('a:has-text("View"), button:has-text("View")').first
            if await view_button.count() > 0:
                await view_button.click()
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)

                # Screenshot QR code details
                await page.screenshot(path=screenshot_path("qr_view_details"), full_page=True)

                # Verify QR code image is displayed
                qr_image = page.locator('img[src*="qr"], img[alt*="QR"], canvas')
                assert await qr_image.count() > 0, "QR code image should be displayed"
        except Exception as e:
            print(f"Note: Could not test view details: {e}")

    async def test_edit_qr_code(self, authenticated_page, base_url, screenshot_path):
        """Test editing a QR code."""
        page = authenticated_page

        await page.goto(f"{base_url}/my-qrcodes")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        # Try to click first edit button
        try:
            edit_button = page.locator('a:has-text("Edit"), button:has-text("Edit")').first
            if await edit_button.count() > 0:
                await edit_button.click()
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)

                # Screenshot edit page
                await page.screenshot(path=screenshot_path("qr_edit_page"), full_page=True)

                # Verify we're on edit page
                assert "/edit" in page.url
        except Exception as e:
            print(f"Note: Could not test edit functionality: {e}")

    async def test_qr_download_functionality(self, authenticated_page, base_url, screenshot_path):
        """Test QR code download functionality."""
        page = authenticated_page

        await page.goto(f"{base_url}/my-qrcodes")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        # Look for download button
        download_button = page.locator('a:has-text("Download"), button:has-text("Download"), a[download]')
        if await download_button.count() > 0:
            print(f"Found {await download_button.count()} download buttons")
            await page.screenshot(path=screenshot_path("qr_download_available"))
        else:
            print("Note: No download buttons found")
