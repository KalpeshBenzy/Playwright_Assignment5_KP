"""TASK 3: DemoWebShop. Each small task has its own test."""
import pytest
from pathlib import Path
from urllib.parse import urlsplit
from playwright.async_api import async_playwright
from utils.config import WEBSHOP, value


@pytest.mark.live
async def test_13_webshop_search_visible(page):
    await page.goto(WEBSHOP)
    assert await page.locator("#small-searchterms").is_visible()
    assert await page.locator("input.search-box-button").is_visible()
    assert await page.locator(".product-item").count() > 0


@pytest.mark.live
async def test_14_webshop_browser_events(page):
    events = []
    page.on("console", lambda msg: events.append("console"))
    page.on("pageerror", lambda error: events.append("pageerror"))
    page.on("request", lambda req: events.append("request"))
    page.on("response", lambda res: events.append("response"))
    await page.goto(WEBSHOP)
    assert "request" in events
    assert "response" in events
    print("Event types observed:", sorted(set(events)))


async def test_15_local_iframe_for_learning(page):
    # No need to guess if DemoWebShop has a live iframe.
    # This small local example teaches how to find text inside a frame.
    await page.set_content('<iframe title="demo frame" srcdoc="<p>Inside the frame</p>"></iframe>')
    frame = page.frame_locator('iframe[title="demo frame"]')
    assert await frame.get_by_text("Inside the frame").is_visible()


async def test_16_dynamic_iframe_for_learning(page):
    await page.set_content('<div id="here"></div>')
    await page.evaluate('document.querySelector("#here").innerHTML = `<iframe title="late" srcdoc="<p>Loaded</p>"></iframe>`')
    frame = page.frame_locator('iframe[title="late"]')
    await frame.get_by_text("Loaded").wait_for()
    assert await frame.get_by_text("Loaded").is_visible()


@pytest.mark.live
async def test_17_webshop_add_to_cart(page):
    await page.goto(WEBSHOP + "books")
    await page.locator(".product-item .product-title a").first.click()
    await page.locator("input[id^='add-to-cart-button']").first.click()
    await page.locator(".cart-qty").wait_for()
    count = (await page.locator(".cart-qty").inner_text()).strip("() ")
    assert int(count) > 0, "Shopping cart did not update"
    await page.screenshot(path="artifacts/screenshots/webshop_cart.png", full_page=True)


@pytest.mark.live
async def test_18_webshop_observed_api_response(page):
    # A safe read-only homepage request is used; this is not a claim of a JSON API.
    response = await page.goto(WEBSHOP)
    assert response is not None
    assert response.status == 200
    assert "text/html" in response.headers.get("content-type", "")





@pytest.mark.live
async def test_20_webshop_save_and_reuse_session(page):
    email = value("WEBSHOP_EMAIL")
    password = value("WEBSHOP_PASSWORD")
    if not email or not password:
        pytest.skip("Set your own DemoWebShop credentials in .env")
    await page.goto(WEBSHOP + "login")
    await page.locator("#Email").fill(email)
    await page.locator("#Password").fill(password)
    await page.locator("input.login-button").click()
    await page.locator("a.ico-logout").wait_for()
    file = Path("auth/webshop_state.json")
    file.parent.mkdir(exist_ok=True)
    await page.context.storage_state(path=str(file))
    # Open a NEW context and test reuse without another login.
    browser = page.context.browser
    assert browser is not None
    new_context = await browser.new_context(storage_state=str(file))
    new_page = await new_context.new_page()
    await new_page.goto(WEBSHOP)
    assert await new_page.locator("a.ico-logout").is_visible(), "Saved state did not log in"
    await new_context.close()


async def test_21_local_dummy_upload(page):
    # This local controlled page shows upload syntax safely.
    await page.set_content('<input type="file" id="upload">')
    await page.locator("#upload").set_input_files("test_data/sample_upload.txt")
    filename = await page.locator("#upload").evaluate("el => el.files[0].name")
    assert filename == "sample_upload.txt"


async def test_22_local_dummy_download(page):
    # Test download only on a controlled local page, not a guessed live link.
    html = '<a id="download" download="sample.txt" href="data:text/plain,hello">Download</a>'
    await page.set_content(html)
    async with page.expect_download() as download_info:
        await page.locator("#download").click()
    download = await download_info.value
    assert download.suggested_filename == "sample.txt"
    await download.save_as("artifacts/reports/sample.txt")
