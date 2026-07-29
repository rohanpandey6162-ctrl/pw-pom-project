"""
Cart page test suite.
Covers: added items appear in cart, item removal, and cart -> inventory navigation.
"""
import pytest
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

BACKPACK = "sauce-labs-backpack"
BACKPACK_NAME = "Sauce Labs Backpack"


@pytest.mark.cart
@pytest.mark.regression
class TestCart:

    @pytest.mark.smoke
    def test_added_item_appears_in_cart(
        self, logged_in_inventory_page: InventoryPage, cart_page: CartPage
    ):
        logged_in_inventory_page.add_to_cart(BACKPACK)
        logged_in_inventory_page.go_to_cart()
        assert BACKPACK_NAME in cart_page.get_item_names()

    def test_remove_item_from_cart(
        self, logged_in_inventory_page: InventoryPage, cart_page: CartPage
    ):
        logged_in_inventory_page.add_to_cart(BACKPACK)
        logged_in_inventory_page.go_to_cart()
        cart_page.remove_item(BACKPACK)
        assert cart_page.get_item_count() == 0

    def test_continue_shopping_returns_to_inventory(
        self, logged_in_inventory_page: InventoryPage, cart_page: CartPage
    ):
        logged_in_inventory_page.go_to_cart()
        cart_page.continue_shopping()
        cart_page.assert_url_contains("inventory.html")
