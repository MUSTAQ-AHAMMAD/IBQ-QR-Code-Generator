#!/usr/bin/env python3
"""
Comprehensive accessibility testing using Axe.
Tests WCAG 2.1 compliance across all pages.
"""
import asyncio
import json
import os
from playwright.async_api import async_playwright
from axe_playwright_python.async_playwright import Axe
from datetime import datetime

BASE_URL = os.getenv("TEST_BASE_URL", "http://127.0.0.1:5000")
REPORTS_DIR = "/home/runner/work/IBQ-QR-Code-Generator/IBQ-QR-Code-Generator/qa-reports/accessibility"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

PAGES_TO_TEST = [
    ("/", "homepage"),
    ("/login", "login"),
    ("/register", "register"),
    ("/dashboard", "dashboard", True),
    ("/generate", "qr_generate", True),
    ("/my-qrcodes", "my_qrcodes", True),
    ("/brands", "brands", True),
    ("/templates", "templates", True),
    ("/settings/profile", "settings_profile", True),
    ("/help", "help", True),
]


async def login(page):
    """Login to the application."""
    await page.goto(f"{BASE_URL}/login")
    await page.wait_for_load_state('networkidle')
    await page.fill('input[name="username"]', ADMIN_USERNAME)
    await page.fill('input[name="password"]', ADMIN_PASSWORD)
    await page.click('input[type="submit"]')
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)


async def test_page_accessibility(page, url, name):
    """Test accessibility for a single page."""
    print(f"  Testing {name}...")

    await page.goto(f"{BASE_URL}{url}")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(1)

    # Run Axe accessibility test
    axe = Axe()
    results = await axe.run(page)

    return {
        "page": name,
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "violations": results.violations,
        "passes": results.passes,
        "incomplete": results.incomplete,
        "inapplicable": results.inapplicable,
        "violation_count": len(results.violations),
        "pass_count": len(results.passes),
    }


async def generate_accessibility_report(all_results):
    """Generate comprehensive accessibility report."""
    print("\n=== Generating Accessibility Report ===")

    total_violations = sum(r["violation_count"] for r in all_results)
    total_passes = sum(r["pass_count"] for r in all_results)

    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_pages_tested": len(all_results),
            "total_violations": total_violations,
            "total_passes": total_passes,
            "compliance_score": round((total_passes / (total_passes + total_violations) * 100), 2) if (total_passes + total_violations) > 0 else 0,
        },
        "pages": all_results,
    }

    # Save JSON report
    json_path = os.path.join(REPORTS_DIR, "accessibility_report.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    # Generate markdown report
    md_path = os.path.join(REPORTS_DIR, "accessibility_report.md")
    with open(md_path, "w") as f:
        f.write("# Accessibility Testing Report\n\n")
        f.write(f"**Generated:** {report['timestamp']}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Pages Tested:** {report['summary']['total_pages_tested']}\n")
        f.write(f"- **Total Violations:** {report['summary']['total_violations']}\n")
        f.write(f"- **Total Passes:** {report['summary']['total_passes']}\n")
        f.write(f"- **Compliance Score:** {report['summary']['compliance_score']}%\n\n")

        f.write("## Pages Tested\n\n")
        for page_result in all_results:
            f.write(f"### {page_result['page']}\n\n")
            f.write(f"- **URL:** `{page_result['url']}`\n")
            f.write(f"- **Violations:** {page_result['violation_count']}\n")
            f.write(f"- **Passes:** {page_result['pass_count']}\n\n")

            if page_result['violations']:
                f.write("#### Violations\n\n")
                for violation in page_result['violations']:
                    f.write(f"- **{violation['id']}** ({violation['impact']}): {violation['description']}\n")
                    f.write(f"  - Help: {violation.get('helpUrl', 'N/A')}\n")
                    f.write(f"  - Occurrences: {len(violation['nodes'])}\n\n")

    print(f"  Accessibility report saved:")
    print(f"    JSON: {json_path}")
    print(f"    Markdown: {md_path}")
    print(f"  Compliance Score: {report['summary']['compliance_score']}%")


async def main():
    """Main function to run accessibility tests."""
    print("=" * 60)
    print("IBQ QR Code Generator - Accessibility Testing")
    print("=" * 60)

    os.makedirs(REPORTS_DIR, exist_ok=True)

    all_results = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Inject Axe
        await page.goto(f"{BASE_URL}/")
        await page.wait_for_load_state('networkidle')

        print("\n=== Testing Pages ===")

        for page_info in PAGES_TO_TEST:
            url = page_info[0]
            name = page_info[1]
            requires_auth = page_info[2] if len(page_info) > 2 else False

            try:
                if requires_auth and not any("dashboard" in r["url"] for r in all_results):
                    await login(page)

                result = await test_page_accessibility(page, url, name)
                all_results.append(result)

                print(f"    Violations: {result['violation_count']}, Passes: {result['pass_count']}")
            except Exception as e:
                print(f"  Error testing {name}: {e}")

        await browser.close()

    # Generate report
    await generate_accessibility_report(all_results)

    print("\n" + "=" * 60)
    print("✓ Accessibility testing completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
