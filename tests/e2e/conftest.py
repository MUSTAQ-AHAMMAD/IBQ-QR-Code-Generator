"""
Pytest configuration and fixtures for E2E tests.
"""
import pytest
import os
from playwright.async_api import async_playwright
from datetime import datetime

# Base URL for testing
BASE_URL = os.getenv("TEST_BASE_URL", "http://127.0.0.1:5000")

# Test credentials
ADMIN_USERNAME = os.getenv("TEST_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("TEST_ADMIN_PASSWORD", "admin123")

# Screenshot and report directories
SCREENSHOTS_DIR = "/home/runner/work/IBQ-QR-Code-Generator/IBQ-QR-Code-Generator/qa-reports/screenshots"
ERRORS_DIR = "/home/runner/work/IBQ-QR-Code-Generator/IBQ-QR-Code-Generator/qa-reports/errors"
PERFORMANCE_DIR = "/home/runner/work/IBQ-QR-Code-Generator/IBQ-QR-Code-Generator/qa-reports/performance"
ACCESSIBILITY_DIR = "/home/runner/work/IBQ-QR-Code-Generator/IBQ-QR-Code-Generator/qa-reports/accessibility"


@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for the application."""
    return BASE_URL


@pytest.fixture(scope="session")
def admin_credentials():
    """Return admin credentials."""
    return {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }


@pytest.fixture(scope="function")
async def browser():
    """Create a browser instance for testing."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()


@pytest.fixture(scope="function")
async def page(browser):
    """Create a new page for testing."""
    context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = await context.new_page()

    # Setup console error logging
    page.on("console", lambda msg: log_console_message(msg))
    page.on("pageerror", lambda err: log_page_error(err))

    yield page
    await page.close()


@pytest.fixture(scope="function")
async def mobile_page(browser):
    """Create a mobile page for responsive testing."""
    context = await browser.new_context(
        viewport={'width': 375, 'height': 812},
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
    )
    page = await context.new_page()

    # Setup console error logging
    page.on("console", lambda msg: log_console_message(msg))
    page.on("pageerror", lambda err: log_page_error(err))

    yield page
    await page.close()


@pytest.fixture(scope="function")
async def tablet_page(browser):
    """Create a tablet page for responsive testing."""
    context = await browser.new_context(
        viewport={'width': 768, 'height': 1024},
        user_agent='Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
    )
    page = await context.new_page()

    # Setup console error logging
    page.on("console", lambda msg: log_console_message(msg))
    page.on("pageerror", lambda err: log_page_error(err))

    yield page
    await page.close()


@pytest.fixture(scope="function")
async def authenticated_page(page, base_url, admin_credentials):
    """Create an authenticated page."""
    await page.goto(f"{base_url}/login")
    await page.wait_for_load_state('networkidle')

    await page.fill('input[name="username"]', admin_credentials["username"])
    await page.fill('input[name="password"]', admin_credentials["password"])
    await page.click('input[type="submit"]')
    await page.wait_for_load_state('networkidle')

    return page


def log_console_message(msg):
    """Log console messages to error directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(ERRORS_DIR, f"console_{timestamp}.log")

    os.makedirs(ERRORS_DIR, exist_ok=True)

    with open(log_file, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg.type}: {msg.text}\n")


def log_page_error(err):
    """Log page errors to error directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(ERRORS_DIR, f"page_error_{timestamp}.log")

    os.makedirs(ERRORS_DIR, exist_ok=True)

    with open(log_file, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] Page Error: {str(err)}\n")


@pytest.fixture(scope="function")
def screenshot_path():
    """Generate a screenshot path based on test name."""
    def _screenshot_path(test_name, suffix=""):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{suffix}_{timestamp}.png" if suffix else f"{test_name}_{timestamp}.png"
        return os.path.join(SCREENSHOTS_DIR, filename)
    return _screenshot_path


@pytest.fixture(scope="session", autouse=True)
def setup_directories():
    """Create all required directories."""
    directories = [
        SCREENSHOTS_DIR,
        os.path.join(SCREENSHOTS_DIR, "desktop"),
        os.path.join(SCREENSHOTS_DIR, "mobile"),
        os.path.join(SCREENSHOTS_DIR, "tablet"),
        os.path.join(SCREENSHOTS_DIR, "dark-mode"),
        os.path.join(SCREENSHOTS_DIR, "light-mode"),
        ERRORS_DIR,
        PERFORMANCE_DIR,
        ACCESSIBILITY_DIR,
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
