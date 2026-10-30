"""Small API helper: use simple functions instead of a complicated framework."""
import asyncio


async def get_with_retry(request, url, tries=3):
    """Retry GET for temporary failures. Never retry CREATE automatically."""
    response = None
    for attempt in range(tries):
        response = await request.get(url)
        if response.status not in [429, 500, 502, 503, 504]:
            return response
        if attempt < tries - 1:
            retry_after = response.headers.get("retry-after", "")
            if retry_after.isdigit():
                pause = min(int(retry_after), 5)
            else:
                pause = 1
            await asyncio.sleep(pause)
    return response


def check_json_fields(data, fields):
    assert isinstance(data, dict), "Expected a JSON object"
    for field in fields:
        assert field in data, "Missing field: " + field


def check_response_type(response, expected):
    content_type = response.headers.get("content-type", "")
    assert expected in content_type.lower(), "Wrong content type: " + content_type


async def create_once(request, url, params):
    """Send a create request ONLY once, to avoid duplicate demo accounts."""
    return await request.post(url, params=params)
