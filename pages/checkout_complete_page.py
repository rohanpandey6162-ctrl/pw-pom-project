"""
Page Object: Checkout Complete Page
https://www.saucedemo.com/checkout-complete.html
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    # ---------- Locators ----------
    URL = "/checkout-complete.html"
    COMPLETE_HEADER = ".complete-header"
    BACK_HOME_BUTTON = "#back-to-products"

    def __init__(self, page: Page):
        super().__init__(page)

    # ---------- State ----------
    def get_confirmation_message(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    # ---------- Actions ----------
    def back_to_products(self):
        self.click(self.BACK_HOME_BUTTON)
        return self
