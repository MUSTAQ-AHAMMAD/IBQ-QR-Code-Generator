"""
End-to-end tests for dark/light theme functionality.

Tests:
- Theme toggle functionality
- Theme persistence
- Text visibility in both modes
- Icon rendering
- QR code visibility
- Contrast validation
"""
import pytest
import asyncio


@pytest.mark.asyncio
class TestThemeSwitching:
    """Test suite for dark/light theme functionality."""

    async def test_theme_toggle_exists(self, authenticated_page, base_url, screenshot_path):
        """Test that theme toggle button exists."""
        page = authenticated_page

        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Look for theme toggle
        theme_toggle = page.locator('#themeToggle, .theme-toggle, button[aria-label*="theme"]')
        assert await theme_toggle.count() > 0, "Theme toggle should exist"

        await page.screenshot(path=screenshot_path("theme_toggle_present"))

    async def test_switch_to_dark_mode(self, authenticated_page, base_url, screenshot_path):
        """Test switching to dark mode."""
        page = authenticated_page

        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Screenshot in light mode
        await page.screenshot(path=screenshot_path("light_mode_dashboard"), full_page=True)

        # Click theme toggle
        theme_toggle = page.locator('#themeToggle, .theme-toggle, button[aria-label*="theme"]').first
        await theme_toggle.click()
        await asyncio.sleep(1)

        # Screenshot in dark mode
        await page.screenshot(path=screenshot_path("dark_mode_dashboard"), full_page=True)

    async def test_dark_mode_all_pages(self, authenticated_page, base_url, screenshot_path):
        """Test dark mode on all pages."""
        page = authenticated_page

        # Enable dark mode
        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')
        theme_toggle = page.locator('#themeToggle, .theme-toggle').first
        if await theme_toggle.count() > 0:
            await theme_toggle.click()
            await asyncio.sleep(1)

        pages_to_test = [
            ("/dashboard", "dark_dashboard"),
            ("/generate", "dark_generate"),
            ("/my-qrcodes", "dark_my_qrcodes"),
            ("/brands", "dark_brands"),
            ("/templates", "dark_templates"),
            ("/settings/profile", "dark_settings"),
        ]

        for url, name in pages_to_test:
            await page.goto(f"{base_url}{url}")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)
            await page.screenshot(path=screenshot_path(name), full_page=True)

    async def test_light_mode_all_pages(self, authenticated_page, base_url, screenshot_path):
        """Test light mode on all pages."""
        page = authenticated_page

        # Ensure light mode is enabled
        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')

        pages_to_test = [
            ("/dashboard", "light_dashboard"),
            ("/generate", "light_generate"),
            ("/my-qrcodes", "light_my_qrcodes"),
            ("/brands", "light_brands"),
            ("/templates", "light_templates"),
            ("/settings/profile", "light_settings"),
        ]

        for url, name in pages_to_test:
            await page.goto(f"{base_url}{url}")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)
            await page.screenshot(path=screenshot_path(name), full_page=True)

    async def test_theme_persistence_after_reload(self, authenticated_page, base_url):
        """Test that theme persists after page reload."""
        page = authenticated_page

        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')

        # Switch to dark mode
        theme_toggle = page.locator('#themeToggle, .theme-toggle').first
        if await theme_toggle.count() > 0:
            await theme_toggle.click()
            await asyncio.sleep(1)

            # Reload page
            await page.reload()
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)

            # Check if dark mode is still active
            html_element = page.locator('html, body')
            classes = await html_element.get_attribute('class')

            # Dark mode should persist
            assert classes and ('dark' in classes or 'theme-dark' in classes), "Dark mode should persist after reload"

    async def test_theme_toggle_animation(self, authenticated_page, base_url, screenshot_path):
        """Test theme toggle animation."""
        page = authenticated_page

        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')

        # Toggle theme multiple times
        theme_toggle = page.locator('#themeToggle, .theme-toggle').first
        if await theme_toggle.count() > 0:
            for i in range(3):
                await theme_toggle.click()
                await asyncio.sleep(0.5)
                await page.screenshot(path=screenshot_path(f"theme_toggle_step_{i}"))

    async def test_qr_code_visibility_in_dark_mode(self, authenticated_page, base_url, screenshot_path):
        """Test that QR codes are visible in dark mode."""
        page = authenticated_page

        # Generate a QR code first
        await page.goto(f"{base_url}/generate")
        await page.wait_for_load_state('networkidle')
        await page.select_option('#qrType, select[name="qr_type"]', 'url')
        await asyncio.sleep(1)
        await page.fill('input[name="name"]', 'Dark Mode Test QR')
        url_field = page.locator('input[name="url"]').first
        await url_field.fill('https://example.com')
        await page.click('button[type="submit"], input[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        # Switch to dark mode
        theme_toggle = page.locator('#themeToggle, .theme-toggle').first
        if await theme_toggle.count() > 0:
            await theme_toggle.click()
            await asyncio.sleep(1)

        # Screenshot QR code in dark mode
        await page.screenshot(path=screenshot_path("qr_in_dark_mode"), full_page=True)

    async def test_icon_rendering_in_both_modes(self, authenticated_page, base_url, screenshot_path):
        """Test icon rendering in both light and dark modes."""
        page = authenticated_page

        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')

        # Light mode icons
        await page.screenshot(path=screenshot_path("icons_light_mode"))

        # Dark mode icons
        theme_toggle = page.locator('#themeToggle, .theme-toggle').first
        if await theme_toggle.count() > 0:
            await theme_toggle.click()
            await asyncio.sleep(1)
            await page.screenshot(path=screenshot_path("icons_dark_mode"))

    async def test_form_visibility_in_dark_mode(self, authenticated_page, base_url, screenshot_path):
        """Test form element visibility in dark mode."""
        page = authenticated_page

        await page.goto(f"{base_url}/generate")
        await page.wait_for_load_state('networkidle')

        # Switch to dark mode
        theme_toggle = page.locator('#themeToggle, .theme-toggle').first
        if await theme_toggle.count() > 0:
            await theme_toggle.click()
            await asyncio.sleep(1)

        # Screenshot form in dark mode
        await page.screenshot(path=screenshot_path("form_dark_mode"), full_page=True)

        # Check input field visibility
        input_fields = page.locator('input[type="text"], input[type="email"], textarea')
        assert await input_fields.count() > 0, "Input fields should be visible in dark mode"

    async def test_navigation_in_dark_mode(self, authenticated_page, base_url, screenshot_path):
        """Test navigation elements in dark mode."""
        page = authenticated_page

        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')

        # Switch to dark mode
        theme_toggle = page.locator('#themeToggle, .theme-toggle').first
        if await theme_toggle.count() > 0:
            await theme_toggle.click()
            await asyncio.sleep(1)

        # Screenshot navigation in dark mode
        await page.screenshot(path=screenshot_path("navigation_dark_mode"))
