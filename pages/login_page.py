"""
Page Object: Login Page
https://www.saucedemo.com/
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    # ---------- Locators ----------
    URL = "/"
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page):
        super().__init__(page)

    # ---------- Actions ----------
    def open(self, base_url: str):
        self.goto(f"{base_url}{self.URL}")
        return self

    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
