"""
End-to-end tests for responsive design across different devices.

Tests:
- Desktop viewport (1920x1080)
- Laptop viewport (1366x768)
- Tablet viewport (768x1024)
- Mobile viewport (375x812)
- Navigation responsiveness
- Layout adaptation
"""
import pytest
import asyncio


@pytest.mark.asyncio
class TestResponsiveDesign:
    """Test suite for responsive design validation."""

    async def test_desktop_viewport(self, authenticated_page, base_url, screenshot_path):
        """Test application on desktop viewport."""
        page = authenticated_page
        await page.set_viewport_size({'width': 1920, 'height': 1080})

        pages_to_test = [
            ("/dashboard", "desktop_dashboard"),
            ("/generate", "desktop_generate"),
            ("/my-qrcodes", "desktop_my_qrcodes"),
            ("/brands", "desktop_brands"),
            ("/templates", "desktop_templates"),
        ]

        for url, name in pages_to_test:
            await page.goto(f"{base_url}{url}")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)
            await page.screenshot(path=screenshot_path(name), full_page=True)

    async def test_laptop_viewport(self, authenticated_page, base_url, screenshot_path):
        """Test application on laptop viewport."""
        page = authenticated_page
        await page.set_viewport_size({'width': 1366, 'height': 768})

        pages_to_test = [
            ("/dashboard", "laptop_dashboard"),
            ("/generate", "laptop_generate"),
            ("/my-qrcodes", "laptop_my_qrcodes"),
        ]

        for url, name in pages_to_test:
            await page.goto(f"{base_url}{url}")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)
            await page.screenshot(path=screenshot_path(name), full_page=True)

    async def test_tablet_viewport(self, tablet_page, base_url, screenshot_path):
        """Test application on tablet viewport."""
        page = tablet_page

        # Login first
        await page.goto(f"{base_url}/login")
        await page.wait_for_load_state('networkidle')
        await page.fill('input[name="username"]', 'admin')
        await page.fill('input[name="password"]', 'admin123')
        await page.click('input[type="submit"]')
        await page.wait_for_load_state('networkidle')

        pages_to_test = [
            ("/dashboard", "tablet_dashboard"),
            ("/generate", "tablet_generate"),
            ("/my-qrcodes", "tablet_my_qrcodes"),
        ]

        for url, name in pages_to_test:
            await page.goto(f"{base_url}{url}")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)
            await page.screenshot(path=screenshot_path(name), full_page=True)

    async def test_mobile_viewport(self, mobile_page, base_url, screenshot_path):
        """Test application on mobile viewport."""
        page = mobile_page

        # Login first
        await page.goto(f"{base_url}/login")
        await page.wait_for_load_state('networkidle')
        await page.fill('input[name="username"]', 'admin')
        await page.fill('input[name="password"]', 'admin123')
        await page.click('input[type="submit"]')
        await page.wait_for_load_state('networkidle')

        pages_to_test = [
            ("/dashboard", "mobile_dashboard"),
            ("/generate", "mobile_generate"),
            ("/my-qrcodes", "mobile_my_qrcodes"),
        ]

        for url, name in pages_to_test:
            await page.goto(f"{base_url}{url}")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)
            await page.screenshot(path=screenshot_path(name), full_page=True)

    async def test_mobile_navigation_menu(self, mobile_page, base_url, screenshot_path):
        """Test mobile navigation menu functionality."""
        page = mobile_page

        # Login first
        await page.goto(f"{base_url}/login")
        await page.wait_for_load_state('networkidle')
        await page.fill('input[name="username"]', 'admin')
        await page.fill('input[name="password"]', 'admin123')
        await page.click('input[type="submit"]')
        await page.wait_for_load_state('networkidle')

        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')

        # Screenshot before opening menu
        await page.screenshot(path=screenshot_path("mobile_menu_closed"))

        # Try to find and click hamburger menu
        try:
            hamburger = page.locator('.navbar-toggler, .menu-toggle, button[aria-label*="menu"]').first
            if await hamburger.count() > 0:
                await hamburger.click()
                await asyncio.sleep(1)

                # Screenshot with menu open
                await page.screenshot(path=screenshot_path("mobile_menu_open"))
        except Exception as e:
            print(f"Note: Could not test mobile menu: {e}")

    async def test_tablet_layout_adaptation(self, tablet_page, base_url, screenshot_path):
        """Test layout adaptation on tablet."""
        page = tablet_page

        # Login
        await page.goto(f"{base_url}/login")
        await page.wait_for_load_state('networkidle')
        await page.fill('input[name="username"]', 'admin')
        await page.fill('input[name="password"]', 'admin123')
        await page.click('input[type="submit"]')
        await page.wait_for_load_state('networkidle')

        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Screenshot tablet dashboard
        await page.screenshot(path=screenshot_path("tablet_layout_dashboard"), full_page=True)

        # Check if sidebar is present
        sidebar = page.locator('.sidebar, nav.sidebar, aside')
        if await sidebar.count() > 0:
            print("Sidebar found on tablet view")

    async def test_responsive_tables(self, authenticated_page, base_url, screenshot_path):
        """Test responsive table behavior."""
        page = authenticated_page

        # Test on mobile
        await page.set_viewport_size({'width': 375, 'height': 812})
        await page.goto(f"{base_url}/my-qrcodes")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        await page.screenshot(path=screenshot_path("mobile_table_view"), full_page=True)

    async def test_responsive_cards(self, authenticated_page, base_url, screenshot_path):
        """Test responsive card layouts."""
        page = authenticated_page

        viewports = [
            ({'width': 1920, 'height': 1080}, "desktop"),
            ({'width': 768, 'height': 1024}, "tablet"),
            ({'width': 375, 'height': 812}, "mobile"),
        ]

        for viewport, name in viewports:
            await page.set_viewport_size(viewport)
            await page.goto(f"{base_url}/brands")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)

            await page.screenshot(path=screenshot_path(f"responsive_cards_{name}"), full_page=True)

    async def test_form_responsiveness(self, authenticated_page, base_url, screenshot_path):
        """Test form responsiveness on different viewports."""
        page = authenticated_page

        viewports = [
            ({'width': 1920, 'height': 1080}, "desktop"),
            ({'width': 768, 'height': 1024}, "tablet"),
            ({'width': 375, 'height': 812}, "mobile"),
        ]

        for viewport, name in viewports:
            await page.set_viewport_size(viewport)
            await page.goto(f"{base_url}/generate")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)

            await page.screenshot(path=screenshot_path(f"responsive_form_{name}"), full_page=True)
