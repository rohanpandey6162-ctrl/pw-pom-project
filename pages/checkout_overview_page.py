"""
Page Object: Checkout Step Two - Order Overview
https://www.saucedemo.com/checkout-step-two.html
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    # ---------- Locators ----------
    URL = "/checkout-step-two.html"
    ITEM_TOTAL = ".summary_subtotal_label"
    TAX = ".summary_tax_label"
    TOTAL = ".summary_total_label"
    FINISH_BUTTON = "#finish"
    CANCEL_BUTTON = "#cancel"

    def __init__(self, page: Page):
        super().__init__(page)

    # ---------- State ----------
    def get_item_total(self) -> str:
        return self.get_text(self.ITEM_TOTAL)

    def get_tax(self) -> str:
        return self.get_text(self.TAX)

    def get_total(self) -> str:
        return self.get_text(self.TOTAL)

    # ---------- Actions ----------
    def finish(self):
        self.click(self.FINISH_BUTTON)
        return self

    def cancel(self):
        self.click(self.CANCEL_BUTTON)
        return self
