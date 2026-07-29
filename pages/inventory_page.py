"""
Page Object: Inventory (Products) Page
https://www.saucedemo.com/inventory.html
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    # ---------- Locators ----------
    URL = "/inventory.html"
    PAGE_TITLE = ".title"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"
    SORT_DROPDOWN = ".product_sort_container"
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page):
        super().__init__(page)

    # ---------- State ----------
    def is_loaded(self) -> bool:
        return self.get_text(self.PAGE_TITLE) == "Products"

    def get_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def get_item_prices(self) -> list[float]:
        raw = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def get_cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.get_text(self.CART_BADGE))

    # ---------- Actions ----------
    def add_to_cart(self, product_slug: str):
        self.click(f"#add-to-cart-{product_slug}")
        return self

    def remove_from_cart(self, product_slug: str):
        self.click(f"#remove-{product_slug}")
        return self

    def go_to_cart(self):
        self.click(self.CART_LINK)
        return self

    def sort_by(self, option_value: str):
        self.select_option(self.SORT_DROPDOWN, option_value)
        return self

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.wait_for_element(self.LOGOUT_LINK)
        self.click(self.LOGOUT_LINK)
        return self
