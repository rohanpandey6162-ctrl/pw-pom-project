"""
Root conftest.py — shared fixtures available to every test in the suite.
This is what wires Playwright's browser/context/page lifecycle into pytest.
"""
import pytest
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page
from config.config import Config
import os
from datetime import datetime


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright):
    browser_type = getattr(playwright_instance, Config.BROWSER)
    browser = browser_type.launch(
        headless=Config.HEADLESS,
        slow_mo=Config.SLOW_MO,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="reports/videos/" if os.getenv("RECORD_VIDEO") == "true" else None,
    )
    context.set_default_timeout(Config.TIMEOUT)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.tracing.stop()
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function", autouse=True)
def attach_trace_on_failure(request, context: BrowserContext):
    """Saves a Playwright trace zip whenever a test fails — huge time-saver for debugging."""
    yield
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        os.makedirs("reports/traces", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_path = f"reports/traces/{request.node.name}_{timestamp}.zip"
        context.tracing.stop(path=trace_path)
        context.tracing.start(screenshots=True, snapshots=True, sources=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Makes test outcome available to fixtures (needed for screenshot/trace-on-failure)."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, page: Page):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("reports/screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"reports/screenshots/{request.node.name}_{timestamp}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"\nScreenshot saved: {screenshot_path}")
