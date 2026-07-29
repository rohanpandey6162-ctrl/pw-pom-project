"""
Page Object: Checkout Step One - Customer Information
https://www.saucedemo.com/checkout-step-one.html
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    # ---------- Locators ----------
    URL = "/checkout-step-one.html"
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    CANCEL_BUTTON = "#cancel"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page):
        super().__init__(page)

    # ---------- Actions ----------
    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)
        return self

    def cancel(self):
        self.click(self.CANCEL_BUTTON)
        return self

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
