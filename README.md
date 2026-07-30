# Playwright + Python UI Automation Framework (Page Object Model)

An end-to-end UI test automation suite for [SauceDemo](https://www.saucedemo.com/), built with **Playwright**, **Python**, and **pytest**, structured with the **Page Object Model (POM)**.

Covers the full shopping journey: login (incl. locked-out/invalid-credential cases) → inventory (add/remove/sort) → cart → checkout → order confirmation → logout.

## Project Structure

```
pw-pom-project/
├── config/                     # Environment config (URLs, browser, timeouts)
│   └── config.py
├── pages/                      # Page Objects (one class per page/screen)
│   ├── base_page.py            # Shared actions/assertions all pages inherit
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_info_page.py
│   ├── checkout_overview_page.py
│   └── checkout_complete_page.py
├── tests/                      # Test files (pytest)
│   ├── conftest.py             # Page-object fixtures
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
├── utils/                      # Test data generators, helpers
│   ├── test_data.py            # Faker-based random customer data
│   └── sauce_data.py           # SauceDemo's fixed test accounts
├── fixtures/                    # Static test data files (json/csv) if needed
├── reports/                     # HTML reports, screenshots, traces, videos (gitignored)
├── .github/workflows/tests.yml  # CI: runs the suite on every push/PR
├── conftest.py                  # Root fixtures: browser/context/page lifecycle
├── pytest.ini                    # Pytest config (markers, report paths)
├── requirements.txt
├── .env.example
└── .vscode/                      # Workspace settings so VS Code auto-detects pytest
```

## Setup

### 1. Prerequisites
- Python 3.9+
- VS Code with the **Python** extension (and optionally the **Claude Code** extension for AI-assisted dev)

### 2. Create a virtual environment
```bash
python -m venv venv

# Activate it
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
```

> Note: if you're on Windows, also update `.vscode/settings.json` →
> `"python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe"`

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install          # downloads browser binaries (chromium, firefox, webkit)
```

### 4. Configure environment
```bash
cp .env.example .env
# edit .env with your BASE_URL, test credentials, etc.
```

### 5. Open in VS Code
```bash
code .
```
VS Code will pick up `.vscode/settings.json` automatically — this enables:
- pytest as the test runner (Testing sidebar shows all tests, run/debug individually)
- correct interpreter (`venv`) auto-selected
- auto-loading of `.env` values into the test run

If prompted, install the recommended extensions (Python, Pylance, Playwright, Python Test Adapter).

## Running Tests

```bash
# Run everything
pytest

# Run only smoke tests
pytest -m smoke

# Run only login-related tests
pytest -m login

# Run in parallel across 4 workers
pytest -n 4

# Run headed (see the browser) for debugging
HEADLESS=false pytest tests/test_login.py -v

# Re-run only failed tests from last run
pytest --lf
```

Or use the **Testing** sidebar (flask icon) in VS Code — click the play button next to any test, class, or the whole file. Right-click → **Debug Test** to step through with breakpoints.

## Reports & Debugging
- HTML report: `reports/report.html` (auto-generated after every run)
- Failed test screenshots: `reports/screenshots/`
- Failed test traces: `reports/traces/*.zip` — open with `playwright show-trace reports/traces/<file>.zip` for a full timeline, DOM snapshots, and network log of the failure
- Optional video recording: set `RECORD_VIDEO=true` in `.env`

## Adding a New Page Object
1. Create `pages/<page_name>_page.py`, inherit from `BasePage`.
2. Define locators as class constants at the top.
3. Add action methods (`click_x()`, `fill_y()`) — keep assertions out of page objects where possible; put them in tests.
4. Add a fixture for it in `tests/conftest.py`.
5. Write tests in `tests/test_<page_name>.py` using the fixture.

## Markers
Defined in `pytest.ini`:
- `smoke` — quick sanity checks, run on every PR
- `regression` — full suite, run nightly/before release
- `login` / `inventory` / `cart` / `checkout` — feature-based markers

## Test Accounts
SauceDemo ships fixed accounts (see `utils/sauce_data.py`), all using password `secret_sauce`:
- `standard_user` — normal happy-path account (used by default)
- `locked_out_user` — login is rejected
- `problem_user`, `performance_glitch_user`, `error_user`, `visual_user` — available for exploratory/edge-case tests

## CI
`.github/workflows/tests.yml` runs the full suite (4 parallel workers) on every push/PR to `master` and uploads the HTML report/screenshots/traces as a build artifact.
