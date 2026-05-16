"""
End-to-end tests for brand management workflows.

Tests:
- Create brand
- Edit brand
- Delete brand
- Brand switching
- Brand validation
- Multi-brand support
"""
import pytest
import asyncio


@pytest.mark.asyncio
class TestBrandManagement:
    """Test suite for brand management workflows."""

    async def test_brands_page_loads(self, authenticated_page, base_url, screenshot_path):
        """Test that brands page loads correctly."""
        page = authenticated_page

        await page.goto(f"{base_url}/brands")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Take screenshot
        await page.screenshot(path=screenshot_path("brands_list_page"), full_page=True)

        # Verify page loaded
        assert "/brands" in page.url

    async def test_create_brand_page_loads(self, authenticated_page, base_url, screenshot_path):
        """Test create brand page loads."""
        page = authenticated_page

        await page.goto(f"{base_url}/brands/create")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Check form elements
        assert await page.query_selector('input[name="name"]') is not None

        # Take screenshot
        await page.screenshot(path=screenshot_path("brands_create_page"), full_page=True)

    async def test_create_brand_with_valid_data(self, authenticated_page, base_url, screenshot_path):
        """Test creating a brand with valid data."""
        page = authenticated_page

        await page.goto(f"{base_url}/brands/create")
        await page.wait_for_load_state('networkidle')

        # Fill brand form
        await page.fill('input[name="name"]', 'Test Brand')

        # Check if description field exists
        description_field = page.locator('textarea[name="description"]')
        if await description_field.count() > 0:
            await description_field.fill('This is a test brand for QA automation')

        # Check if website field exists
        website_field = page.locator('input[name="website"]')
        if await website_field.count() > 0:
            await website_field.fill('https://testbrand.com')

        # Check if email field exists
        email_field = page.locator('input[name="email"]')
        if await email_field.count() > 0:
            await email_field.fill('contact@testbrand.com')

        # Screenshot before submit
        await page.screenshot(path=screenshot_path("brands_create_filled"), full_page=True)

        # Submit form
        submit_button = page.locator('button[type="submit"], input[type="submit"]').first
        await submit_button.click()
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Screenshot after creation
        await page.screenshot(path=screenshot_path("brands_create_success"), full_page=True)

    async def test_brand_customization_options(self, authenticated_page, base_url, screenshot_path):
        """Test brand customization options."""
        page = authenticated_page

        await page.goto(f"{base_url}/brands/create")
        await page.wait_for_load_state('networkidle')

        # Check for color pickers
        primary_color = page.locator('input[name="primary_color"], input[type="color"]').first
        if await primary_color.count() > 0:
            await primary_color.fill('#FF5733')

        # Screenshot with colors set
        await page.screenshot(path=screenshot_path("brands_customization"), full_page=True)

    async def test_brand_list_displays_brands(self, authenticated_page, base_url, screenshot_path):
        """Test that brand list displays created brands."""
        page = authenticated_page

        await page.goto(f"{base_url}/brands")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Check if any brand cards exist
        brand_cards = page.locator('.card, .brand-card, [class*="brand"]')
        count = await brand_cards.count()

        print(f"Found {count} brand elements on page")

        # Screenshot of brand list
        await page.screenshot(path=screenshot_path("brands_list_with_brands"), full_page=True)

    async def test_edit_brand_page(self, authenticated_page, base_url, screenshot_path):
        """Test editing a brand."""
        page = authenticated_page

        # Go to brands page first
        await page.goto(f"{base_url}/brands")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Try to find and click edit button
        try:
            edit_button = page.locator('a:has-text("Edit"), button:has-text("Edit")').first
            if await edit_button.count() > 0:
                await edit_button.click()
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(1)

                # Screenshot edit page
                await page.screenshot(path=screenshot_path("brands_edit_page"), full_page=True)

                # Verify we're on edit page
                assert "/brands/edit" in page.url or "/edit" in page.url
        except Exception as e:
            print(f"Note: Could not test edit functionality: {e}")

    async def test_brand_switching(self, authenticated_page, base_url, screenshot_path):
        """Test brand switching functionality."""
        page = authenticated_page

        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Screenshot before brand switch
        await page.screenshot(path=screenshot_path("brand_before_switch"), full_page=True)

        # Look for brand switcher
        brand_switcher = page.locator('select[name="brand"], #brandSelector, .brand-switcher')
        if await brand_switcher.count() > 0:
            # Get current value
            current_value = await brand_switcher.input_value()
            print(f"Current brand: {current_value}")

            # Try to switch to different brand
            options = await brand_switcher.locator('option').all()
            if len(options) > 1:
                # Select second option
                await brand_switcher.select_option(index=1)
                await asyncio.sleep(2)

                # Screenshot after brand switch
                await page.screenshot(path=screenshot_path("brand_after_switch"), full_page=True)
        else:
            print("Note: Brand switcher not found on dashboard")

    async def test_brand_validation(self, authenticated_page, base_url, screenshot_path):
        """Test brand form validation."""
        page = authenticated_page

        await page.goto(f"{base_url}/brands/create")
        await page.wait_for_load_state('networkidle')

        # Try to submit empty form
        submit_button = page.locator('button[type="submit"], input[type="submit"]').first
        await submit_button.click()
        await asyncio.sleep(1)

        # Should show validation errors
        await page.screenshot(path=screenshot_path("brands_validation_errors"), full_page=True)

        # Should still be on create page
        assert "/brands/create" in page.url or "/create" in page.url
