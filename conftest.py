import pytest
import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pytest_html import extras as html_extras


# ========================
# HARD BLOCKING PRIVACY POPUP (RUNS ONCE)
# ========================
def wait_and_close_privacy_popup(page, timeout=15000):
    """
    BLOCKING handler:
    - Waits until OneTrust popup appears
    - Closes it
    - Stops execution until done
    - Safe for headless, parallel, CI
    """
    close_btn = page.locator("#close-pc-btn-handler")

    try:
        close_btn.wait_for(state="visible", timeout=timeout)
        close_btn.click(force=True)
        page.wait_for_timeout(300)
        print("Privacy popup detected and closed")
    except PlaywrightTimeoutError:
        print("Privacy popup not shown")


# ========================
# PAGE FIXTURE
# ========================
@pytest.fixture(scope="class")
def page(request):
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=True  # True in CI
    )

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )

    # Reasonable defaults
    context.set_default_timeout(30000)
    context.set_default_navigation_timeout(30000)
    page = context.new_page()
    # Open base URL
    page.goto("https://www.physiciansweekly.com", wait_until="domcontentloaded")
    # Close popup if it appears (no blocking)
    wait_and_close_privacy_popup(page)
    request.node.page = page
    yield page

    # Cleanup
    context.close()
    browser.close()
    playwright.stop()

def pytest_html_report_title(report):
    report.title = "Physician Weekly - Automation Testing Report [Tester : Ashok]"

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([
        ("Project Name", "Physician weekly"),
        ("Tester", "Ashok Kumar"),
    ])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Get page fixture correctly
        page = item.funcargs.get("page", None)
        if page:
            os.makedirs("screenshots", exist_ok=True)
            path = f"screenshots/{item.name}_{int(time.time())}.png"
            try:
                page.screenshot(path=path, full_page=True)
            except Exception as e:
                print("Screenshot capture failed:", e)
            else:
                if not hasattr(report, "extras"):
                    report.extras = []
                report.extras.append(html_extras.image(path))