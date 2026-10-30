"""Simple browser fixture and screenshots on failed tests."""
from pathlib import Path
import os
import pytest
from playwright.async_api import async_playwright
from utils.config import is_live

SCREENSHOTS = Path("artifacts/screenshots")
SCREENSHOTS.mkdir(parents=True, exist_ok=True)


def pytest_collection_modifyitems(items):
    # Live tests are off by default. This prevents accidental API changes.
    if is_live():
        return
    skip = pytest.mark.skip(reason="Set RUN_LIVE=1 in .env to test live demo websites")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip)


@pytest.fixture
async def page():
    async with async_playwright() as playwright:
        browser_path = os.getenv("TEST_CHROMIUM_PATH")
        if browser_path:
            browser = await playwright.chromium.launch(headless=True, executable_path=browser_path, args=["--no-sandbox"])
        else:
            browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        # Failures are reported in pytest output. Tests can also save screenshots.
        print("FAILED:", item.name, "(see pytest failure details)")
