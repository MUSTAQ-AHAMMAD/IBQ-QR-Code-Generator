"""
End-to-end tests for authentication workflows.

Tests:
- Login functionality
- Logout functionality
- Registration
- Password reset
- Session management
- Account lockout
"""
import pytest
import asyncio
from datetime import datetime


@pytest.mark.asyncio
class TestAuthentication:
    """Test suite for authentication workflows."""

    async def test_login_page_loads(self, page, base_url, screenshot_path):
        """Test that login page loads correctly."""
        await page.goto(f"{base_url}/login")
        await page.wait_for_load_state('networkidle')

        # Check page title
        title = await page.title()
        assert "Login" in title or "QR Code Generator" in title

        # Check form elements exist
        assert await page.query_selector('input[name="username"]') is not None
        assert await page.query_selector('input[name="password"]') is not None
        assert await page.query_selector('input[type="submit"]') is not None

        # Take screenshot
        await page.screenshot(path=screenshot_path("auth_login_page"))

    async def test_successful_login(self, page, base_url, admin_credentials, screenshot_path):
        """Test successful login flow."""
        await page.goto(f"{base_url}/login")
        await page.wait_for_load_state('networkidle')

        # Fill login form
        await page.fill('input[name="username"]', admin_credentials["username"])
        await page.fill('input[name="password"]', admin_credentials["password"])

        # Screenshot before submit
        await page.screenshot(path=screenshot_path("auth_login_filled"))

        # Submit form
        await page.click('input[type="submit"]')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1)

        # Verify redirect to dashboard
        assert "/dashboard" in page.url or "/home" in page.url

        # Screenshot after login
        await page.screenshot(path=screenshot_path("auth_login_success"))

    async def test_failed_login_invalid_credentials(self, page, base_url, screenshot_path):
        """Test login with invalid credentials."""
        await page.goto(f"{base_url}/login")
        await page.wait_for_load_state('networkidle')

        # Fill with wrong credentials
        await page.fill('input[name="username"]', "wronguser")
        await page.fill('input[name="password"]', "wrongpass")
        await page.click('input[type="submit"]')
        await page.wait_for_load_state('networkidle')

        # Should stay on login page
        assert "/login" in page.url

        # Screenshot error state
        await page.screenshot(path=screenshot_path("auth_login_failed"))

    async def test_registration_page_loads(self, page, base_url, screenshot_path):
        """Test registration page loads."""
        await page.goto(f"{base_url}/register")
        await page.wait_for_load_state('networkidle')

        # Check registration form elements
        assert await page.query_selector('input[name="username"]') is not None
        assert await page.query_selector('input[name="email"]') is not None
        assert await page.query_selector('input[name="password"]') is not None

        # Take screenshot
        await page.screenshot(path=screenshot_path("auth_registration_page"))

    async def test_logout_functionality(self, authenticated_page, base_url, screenshot_path):
        """Test logout functionality."""
        page = authenticated_page

        # Ensure we're logged in
        await page.goto(f"{base_url}/dashboard")
        await page.wait_for_load_state('networkidle')

        # Find and click logout button/link
        try:
            # Try finding logout link
            logout_link = page.locator('a:has-text("Logout"), a:has-text("Log out"), a:has-text("Sign out")').first
            await logout_link.click()
        except:
            # Alternative: look for logout form
            logout_form = page.locator('form[action*="logout"]').first
            if await logout_form.count() > 0:
                await logout_form.locator('button, input[type="submit"]').first.click()

        await page.wait_for_load_state('networkidle')

        # Should redirect to login page
        assert "/login" in page.url or "/" == page.url

        # Screenshot after logout
        await page.screenshot(path=screenshot_path("auth_logout_success"))

    async def test_session_persistence(self, authenticated_page, base_url):
        """Test that session persists across page navigation."""
        page = authenticated_page

        # Navigate to different pages
        pages_to_test = [
            "/dashboard",
            "/generate",
            "/my-qrcodes",
            "/templates",
        ]

        for test_page in pages_to_test:
            await page.goto(f"{base_url}{test_page}")
            await page.wait_for_load_state('networkidle')

            # Should not redirect to login
            assert "/login" not in page.url
            assert page.url.endswith(test_page)

    async def test_protected_route_redirects_to_login(self, page, base_url):
        """Test that protected routes redirect to login when not authenticated."""
        protected_routes = [
            "/dashboard",
            "/generate",
            "/my-qrcodes",
            "/templates",
            "/settings/profile",
        ]

        for route in protected_routes:
            await page.goto(f"{base_url}{route}")
            await page.wait_for_load_state('networkidle')

            # Should redirect to login
            assert "/login" in page.url

    async def test_password_field_is_masked(self, page, base_url):
        """Test that password field properly masks input."""
        await page.goto(f"{base_url}/login")
        await page.wait_for_load_state('networkidle')

        password_field = page.locator('input[name="password"]')
        input_type = await password_field.get_attribute('type')

        assert input_type == "password"
