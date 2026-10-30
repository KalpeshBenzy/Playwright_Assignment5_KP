
from pathlib import Path
from urllib.parse import urlsplit
import pytest
from utils.config import AMAZON
from playwright.async_api import expect
pytestmark = pytest.mark.live

#TASK 1: Amazon. Run only with RUN_LIVE=1. One test per action.

@pytest.mark.asyncio
async def test_01_amazon_search_is_visible(page):
    # Step 1: Open Amazon
    await page.goto(AMAZON, wait_until="domcontentloaded")

    # Step 2: Find the search box
    search = page.locator("#twotabsearchtextbox")

    assert await search.is_visible(), "Amazon search box was not visible"
    button = page.locator("#nav-search-submit-button")
    assert await button.is_visible(), "Search button was not visible"



@pytest.mark.asyncio
async def test_02_amazon_browser_events(page):
    events = []
    
    page.on("console", lambda msg: events.append("console:" + msg.type))
    page.on("pageerror", lambda error: events.append("pageerror"))
    page.on("request", lambda req: events.append("request:" + req.method + ":" + urlsplit(req.url).path[:80]))
    page.on("response", lambda res: events.append("response:" + str(res.status)))
    page.on("dialog", lambda dialog: events.append("dialog"))
    await page.goto(AMAZON, wait_until="domcontentloaded")
    assert any(event.startswith("request:") for event in events), "No requests were recorded"
    assert any(event.startswith("response:") for event in events), "No responses were recorded"
    print("Observed event types:", sorted({event.split(":")[0] for event in events}))


@pytest.mark.asyncio
async def test_03_amazon_search_book(page):
    await page.goto(AMAZON, wait_until="domcontentloaded")
    await page.locator("#twotabsearchtextbox").fill("python beginner book")
    await page.locator("#nav-search-submit-button").click()
    await page.locator("[data-component-type='s-search-result']").first.wait_for(timeout=20000)
    assert "python" in (await page.title()).lower() or await page.locator("[data-component-type='s-search-result']").count() > 0
    await page.screenshot(path="artifacts/screenshots/amazon_search.png", full_page=True)


@pytest.mark.asyncio
async def test_04_amazon_optional_popup(page):
    await page.goto(AMAZON, wait_until="domcontentloaded")
    # The site may or may not display a consent banner.
    consent = page.get_by_role("button", name="Accept Cookies")
    if await consent.count() > 0 and await consent.first.is_visible():
        await consent.first.click()
    assert await page.locator("#twotabsearchtextbox").is_visible()


@pytest.mark.asyncio
async def test_05_amazon_page_open_and_close_events(page):
    await page.goto(AMAZON, wait_until="domcontentloaded")
    opened = []
    closed = []
    page.context.on("page", lambda new_page: opened.append(new_page))
    # Use a controlled safe link because Amazon may not open tabs predictably.
    await page.evaluate("window.open('about:blank', '_blank')")
    await page.wait_for_timeout(500)
    assert len(opened) > 0, "No new-page event detected"
    new_page = opened[-1]
    new_page.on("close", lambda: closed.append(True))
    await new_page.close()
    assert closed, "Close event was not fired"



