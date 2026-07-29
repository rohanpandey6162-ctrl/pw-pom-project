"""
Base Page - parent class for all Page Objects.
Wraps common Playwright actions with waits, logging, and reusable helpers.
"""
from playwright.sync_api import Page, expect
import logging
import re

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.default_timeout = 10000  # ms

    # ---------- Navigation ----------
    def goto(self, url: str):
        logger.info(f"Navigating to {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    # ---------- Element actions ----------
    def click(self, locator: str):
        logger.info(f"Clicking: {locator}")
        self.page.locator(locator).click(timeout=self.default_timeout)

    def fill(self, locator: str, text: str):
        logger.info(f"Filling '{locator}' with '{text}'")
        el = self.page.locator(locator)
        el.wait_for(state="visible", timeout=self.default_timeout)
        el.fill(text)

    def get_text(self, locator: str) -> str:
        return self.page.locator(locator).inner_text(timeout=self.default_timeout)

    def is_visible(self, locator: str) -> bool:
        return self.page.locator(locator).is_visible()

    def select_option(self, locator: str, value: str):
        self.page.locator(locator).select_option(value)

    def hover(self, locator: str):
        self.page.locator(locator).hover()

    def upload_file(self, locator: str, file_path: str):
        self.page.locator(locator).set_input_files(file_path)

    # ---------- Waits ----------
    def wait_for_element(self, locator: str, state: str = "visible"):
        self.page.locator(locator).wait_for(state=state, timeout=self.default_timeout)

    def wait_for_url(self, url_pattern: str):
        self.page.wait_for_url(url_pattern, timeout=self.default_timeout)

    # ---------- Assertions (wrapping Playwright's expect) ----------
    def assert_visible(self, locator: str):
        expect(self.page.locator(locator)).to_be_visible()

    def assert_text(self, locator: str, text: str):
        expect(self.page.locator(locator)).to_have_text(text)

    def assert_url_contains(self, text: str):
        expect(self.page).to_have_url(re.compile(re.escape(text)))

    # ---------- Utilities ----------
    def screenshot(self, path: str):
        self.page.screenshot(path=path, full_page=True)
