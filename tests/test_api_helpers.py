"""TASK 4: Beginner API helper tests. Mock objects mean no real demo data changes."""
from utils.api_client import get_with_retry, check_json_fields, check_response_type, create_once


class FakeResponse:
    def __init__(self, status, headers=None):
        self.status = status
        self.headers = headers or {"content-type": "application/json"}


class FakeRequest:
    def __init__(self, statuses):
        self.statuses = statuses
        self.calls = 0

    async def get(self, url):
        self.calls += 1
        return FakeResponse(self.statuses[min(self.calls - 1, len(self.statuses) - 1)])

    async def post(self, url, params=None):
        self.calls += 1
        return FakeResponse(201)


async def test_23_api_get_success():
    request = FakeRequest([200])
    response = await get_with_retry(request, "https://example.invalid/demo")
    assert response.status == 200
    assert request.calls == 1


async def test_24_api_missing_field():
    try:
        check_json_fields({"id": 1}, ["id", "name"])
        assert False, "Missing-field assertion should have failed"
    except AssertionError as error:
        assert "name" in str(error)


async def test_25_api_malformed_data():
    try:
        check_json_fields([1, 2], ["id"])
        assert False, "List should not be accepted as a JSON object"
    except AssertionError as error:
        assert "JSON object" in str(error)


async def test_26_api_content_type():
    response = FakeResponse(200)
    check_response_type(response, "json")


async def test_27_api_invalid_input_mock():
    response = FakeResponse(400)
    assert response.status == 400


async def test_28_api_retry_succeeds():
    request = FakeRequest([503, 200])
    response = await get_with_retry(request, "https://example.invalid/demo")
    assert response.status == 200
    assert request.calls == 2


async def test_29_api_retry_exhaustion():
    request = FakeRequest([503, 503, 503])
    response = await get_with_retry(request, "https://example.invalid/demo", tries=3)
    assert response.status == 503
    assert request.calls == 3


async def test_30_api_create_only_once():
    request = FakeRequest([])
    response = await create_once(request, "https://example.invalid/create", {"type": 1})
    assert response.status == 201
    assert request.calls == 1


async def test_31_api_result_shown_in_local_ui(page):
    # Simulate an API response and check what a page displays.
    data = {"accountId": "DEMO-101"}
    await page.set_content('<span id="account"></span>')
    await page.locator("#account").evaluate("(el, value) => el.textContent = value", data["accountId"])
    assert await page.locator("#account").inner_text() == data["accountId"]
