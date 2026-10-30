

Command run in the development environment:

```bash
TEST_CHROMIUM_PATH=/usr/bin/chromium python -m pytest -q --junitxml=artifacts/reports/local_results.xml
```

Result: **31 tests collected, 13 passed, 18 skipped, 0 failed**.

- Offline API mock tests: passed.
- Local iframe, dynamic iframe, file upload and download tests: passed using installed system Chromium.
- Amazon, ParaBank and DemoWebShop live tests: skipped because RUN_LIVE is disabled until the student configures and validates the live demo environment.
- Actual Amazon popup, upload or download support not verified.
- Actual ParaBank create-account API and DemoWebShop real login not executed.

This report is NOT evidence that the live website tests have passed. Run those tests with your own demo credentials after inspecting the current pages and API contract.
