#!/usr/bin/env python3
"""
Comprehensive visual QA testing system.
Detects layout issues, alignment problems, broken elements.
"""
import asyncio
import json
import os
from playwright.async_api import async_playwright
from datetime import datetime

BASE_URL = os.getenv("TEST_BASE_URL", "http://127.0.0.1:5000")
REPORTS_DIR = "/home/runner/work/IBQ-QR-Code-Generator/IBQ-QR-Code-Generator/qa-reports"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


async def login(page):
    """Login to the application."""
    await page.goto(f"{BASE_URL}/login")
    await page.wait_for_load_state('networkidle')
    await page.fill('input[name="username"]', ADMIN_USERNAME)
    await page.fill('input[name="password"]', ADMIN_PASSWORD)
    await page.click('input[type="submit"]')
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(2)


async def detect_layout_issues(page):
    """Detect layout and visual issues on the page."""
    issues = []

    # Check for overlapping elements
    overlapping = await page.evaluate("""
        () => {
            const elements = document.querySelectorAll('*');
            const overlaps = [];

            for (let i = 0; i < elements.length; i++) {
                const el1 = elements[i];
                const rect1 = el1.getBoundingClientRect();

                if (rect1.width === 0 || rect1.height === 0) continue;

                for (let j = i + 1; j < elements.length; j++) {
                    const el2 = elements[j];
                    const rect2 = el2.getBoundingClientRect();

                    if (rect2.width === 0 || rect2.height === 0) continue;

                    // Check if elements overlap
                    if (!(rect1.right < rect2.left ||
                          rect1.left > rect2.right ||
                          rect1.bottom < rect2.top ||
                          rect1.top > rect2.bottom)) {
                        overlaps.push({
                            element1: el1.tagName + (el1.className ? '.' + el1.className.split(' ')[0] : ''),
                            element2: el2.tagName + (el2.className ? '.' + el2.className.split(' ')[0] : '')
                        });
                        if (overlaps.length > 10) break;
                    }
                }
                if (overlaps.length > 10) break;
            }

            return overlaps;
        }
    """)

    if overlapping:
        issues.append({
            "type": "overlapping_elements",
            "severity": "medium",
            "count": len(overlapping),
            "details": overlapping[:5],  # Limit to first 5
        })

    # Check for horizontal overflow
    overflow = await page.evaluate("""
        () => {
            const bodyWidth = document.body.scrollWidth;
            const viewportWidth = window.innerWidth;
            const hasOverflow = bodyWidth > viewportWidth;

            if (hasOverflow) {
                // Find elements causing overflow
                const elements = document.querySelectorAll('*');
                const overflowing = [];

                for (let el of elements) {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > viewportWidth) {
                        overflowing.push({
                            tag: el.tagName,
                            class: el.className,
                            width: rect.width,
                            right: rect.right
                        });
                        if (overflowing.length >= 5) break;
                    }
                }

                return {
                    hasOverflow: true,
                    bodyWidth: bodyWidth,
                    viewportWidth: viewportWidth,
                    overflowingElements: overflowing
                };
            }

            return { hasOverflow: false };
        }
    """)

    if overflow.get("hasOverflow"):
        issues.append({
            "type": "horizontal_overflow",
            "severity": "high",
            "details": overflow,
        })

    # Check for broken images
    broken_images = await page.evaluate("""
        () => {
            const images = document.querySelectorAll('img');
            const broken = [];

            for (let img of images) {
                if (!img.complete || img.naturalWidth === 0) {
                    broken.push({
                        src: img.src,
                        alt: img.alt
                    });
                }
            }

            return broken;
        }
    """)

    if broken_images:
        issues.append({
            "type": "broken_images",
            "severity": "high",
            "count": len(broken_images),
            "details": broken_images,
        })

    # Check for missing alt attributes
    missing_alt = await page.evaluate("""
        () => {
            const images = document.querySelectorAll('img');
            const missing = [];

            for (let img of images) {
                if (!img.alt || img.alt.trim() === '') {
                    missing.push({
                        src: img.src
                    });
                }
            }

            return missing;
        }
    """)

    if missing_alt:
        issues.append({
            "type": "missing_alt_text",
            "severity": "medium",
            "count": len(missing_alt),
            "details": missing_alt[:10],
        })

    # Check for incorrect color contrast
    contrast_issues = await page.evaluate("""
        () => {
            const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, a, button, label');
            const issues = [];

            for (let el of textElements) {
                const style = window.getComputedStyle(el);
                const bgColor = style.backgroundColor;
                const color = style.color;
                const fontSize = parseFloat(style.fontSize);

                // Simple visibility check (not full contrast calculation)
                if (color === bgColor || (color === 'rgba(0, 0, 0, 0)' && bgColor === 'rgba(0, 0, 0, 0)')) {
                    issues.push({
                        tag: el.tagName,
                        class: el.className,
                        text: el.textContent.substring(0, 50),
                        color: color,
                        backgroundColor: bgColor
                    });
                    if (issues.length >= 5) break;
                }
            }

            return issues;
        }
    """)

    if contrast_issues:
        issues.append({
            "type": "contrast_issues",
            "severity": "medium",
            "count": len(contrast_issues),
            "details": contrast_issues,
        })

    # Check for elements outside viewport
    outside_viewport = await page.evaluate("""
        () => {
            const elements = document.querySelectorAll('*');
            const outside = [];
            const viewportHeight = window.innerHeight;
            const viewportWidth = window.innerWidth;

            for (let el of elements) {
                const rect = el.getBoundingClientRect();

                if ((rect.right < 0 || rect.left > viewportWidth ||
                     rect.bottom < 0 || rect.top > viewportHeight) &&
                    rect.width > 0 && rect.height > 0) {
                    outside.push({
                        tag: el.tagName,
                        class: el.className,
                        position: {
                            top: rect.top,
                            left: rect.left
                        }
                    });
                    if (outside.length >= 5) break;
                }
            }

            return outside;
        }
    """)

    if outside_viewport:
        issues.append({
            "type": "elements_outside_viewport",
            "severity": "low",
            "count": len(outside_viewport),
            "details": outside_viewport,
        })

    return issues


async def test_page_visual_qa(page, url, name):
    """Run visual QA tests on a page."""
    print(f"  Testing {name}...")

    await page.goto(f"{BASE_URL}{url}")
    await page.wait_for_load_state('networkidle')
    await asyncio.sleep(1)

    # Detect issues
    issues = await detect_layout_issues(page)

    return {
        "page": name,
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "issues": issues,
        "issue_count": len(issues),
    }


async def generate_visual_qa_report(all_results):
    """Generate visual QA report."""
    print("\n=== Generating Visual QA Report ===")

    total_issues = sum(r["issue_count"] for r in all_results)
    high_severity = sum(
        1 for r in all_results for i in r["issues"] if i.get("severity") == "high"
    )
    medium_severity = sum(
        1 for r in all_results for i in r["issues"] if i.get("severity") == "medium"
    )
    low_severity = sum(
        1 for r in all_results for i in r["issues"] if i.get("severity") == "low"
    )

    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_pages_tested": len(all_results),
            "total_issues": total_issues,
            "high_severity": high_severity,
            "medium_severity": medium_severity,
            "low_severity": low_severity,
        },
        "pages": all_results,
    }

    # Save JSON report
    json_path = os.path.join(REPORTS_DIR, "visual-qa-report.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    # Generate markdown report
    md_path = os.path.join(REPORTS_DIR, "visual-qa-report.md")
    with open(md_path, "w") as f:
        f.write("# Visual QA Testing Report\n\n")
        f.write(f"**Generated:** {report['timestamp']}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Pages Tested:** {report['summary']['total_pages_tested']}\n")
        f.write(f"- **Total Issues:** {report['summary']['total_issues']}\n")
        f.write(f"- **High Severity:** {report['summary']['high_severity']}\n")
        f.write(f"- **Medium Severity:** {report['summary']['medium_severity']}\n")
        f.write(f"- **Low Severity:** {report['summary']['low_severity']}\n\n")

        f.write("## Issue Types Detected\n\n")
        f.write("- Overlapping elements\n")
        f.write("- Horizontal overflow\n")
        f.write("- Broken images\n")
        f.write("- Missing alt text\n")
        f.write("- Contrast issues\n")
        f.write("- Elements outside viewport\n\n")

        f.write("## Pages Tested\n\n")
        for page_result in all_results:
            f.write(f"### {page_result['page']}\n\n")
            f.write(f"- **URL:** `{page_result['url']}`\n")
            f.write(f"- **Issues Found:** {page_result['issue_count']}\n\n")

            if page_result['issues']:
                for issue in page_result['issues']:
                    f.write(f"#### {issue['type'].replace('_', ' ').title()}\n\n")
                    f.write(f"- **Severity:** {issue['severity']}\n")
                    if 'count' in issue:
                        f.write(f"- **Count:** {issue['count']}\n")
                    f.write("\n")

    print(f"  Visual QA report saved:")
    print(f"    JSON: {json_path}")
    print(f"    Markdown: {md_path}")
    print(f"  Total Issues: {total_issues}")


async def main():
    """Main function."""
    print("=" * 60)
    print("IBQ QR Code Generator - Visual QA Testing")
    print("=" * 60)

    os.makedirs(REPORTS_DIR, exist_ok=True)

    PAGES = [
        ("/", "homepage"),
        ("/login", "login"),
        ("/dashboard", "dashboard", True),
        ("/generate", "qr_generate", True),
        ("/my-qrcodes", "my_qrcodes", True),
        ("/brands", "brands", True),
        ("/templates", "templates", True),
    ]

    all_results = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        print("\n=== Testing Pages ===")

        for page_info in PAGES:
            url = page_info[0]
            name = page_info[1]
            requires_auth = page_info[2] if len(page_info) > 2 else False

            try:
                if requires_auth and not any("dashboard" in r["url"] for r in all_results):
                    await login(page)

                result = await test_page_visual_qa(page, url, name)
                all_results.append(result)

                print(f"    Issues: {result['issue_count']}")
            except Exception as e:
                print(f"  Error testing {name}: {e}")

        await browser.close()

    # Generate report
    await generate_visual_qa_report(all_results)

    print("\n" + "=" * 60)
    print("✓ Visual QA testing completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
