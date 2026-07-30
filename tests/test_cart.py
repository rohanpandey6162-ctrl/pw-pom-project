"""
Cart page test suite.
Covers: added items appear in cart, item removal, and cart -> inventory navigation.
"""
import pytest
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from utils.sauce_data import BACKPACK

BACKPACK_NAME = "Sauce Labs Backpack"


@pytest.mark.cart
@pytest.mark.regression
class TestCart:

    @pytest.mark.smoke
    def test_added_item_appears_in_cart(
        self, logged_in_inventory_page: InventoryPage, cart_page: CartPage
    ):
        """An item added from the inventory page shows up by name on the cart page."""
        logged_in_inventory_page.add_to_cart(BACKPACK)
        logged_in_inventory_page.go_to_cart()
        assert BACKPACK_NAME in cart_page.get_item_names()

    def test_remove_item_from_cart(
        self, logged_in_inventory_page: InventoryPage, cart_page: CartPage
    ):
        """Removing an item from the cart page leaves the cart empty."""
        logged_in_inventory_page.add_to_cart(BACKPACK)
        logged_in_inventory_page.go_to_cart()
        cart_page.remove_item(BACKPACK)
        assert cart_page.get_item_count() == 0

    def test_continue_shopping_returns_to_inventory(
        self, logged_in_inventory_page: InventoryPage, cart_page: CartPage
    ):
        """'Continue Shopping' from the cart navigates back to the inventory page."""
        logged_in_inventory_page.go_to_cart()
        cart_page.continue_shopping()
        cart_page.assert_url_contains("inventory.html")
