

1. Unzip the project and choose **File > Open Folder**.
2. Open **Terminal > New Terminal**.
3. Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and copy with `copy .env.example .env`.

## Run

```bash
python -m pytest --collect-only -q
python -m pytest -v
python -m pytest tests/test_api_helpers.py -v
python -m pytest tests/test_demowebshop_frames_session.py -v
```


Run one test at a time:

```bash
python -m pytest tests/test_amazon_events.py::test_01_amazon_search_is_visible -v
python -m pytest tests/test_parabank_api_ui.py::test_08_parabank_login -v
```

## Files

- `tests/test_amazon_events.py` — Task 1, tests 01–07
- `tests/test_parabank_api_ui.py` — Task 2, tests 08–12
- `tests/test_demowebshop_frames_session.py` — Task 3, tests 13–22
- `tests/test_api_helpers.py` — Task 4, tests 23–31
- `utils/api_client.py` — easy GET/retry/response helper
- `utils/config.py` — URLs and environment variables



