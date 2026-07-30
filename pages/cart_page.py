"""
Page Object: Cart Page
https://www.saucedemo.com/cart.html
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    # ---------- Locators ----------
    URL = "/cart.html"
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"

    def __init__(self, page: Page):
        super().__init__(page)

    # ---------- State ----------
    def get_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def get_item_prices(self) -> list[float]:
        raw = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def get_item_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    # ---------- Actions ----------
    def remove_item(self, product_slug: str):
        self.click(f"#remove-{product_slug}")
        return self

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        return self
