"""
Inventory (Products) page test suite.
Covers: add/remove-to-cart badge count, sorting, and logout.
"""
import pytest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.sauce_data import BACKPACK, BIKE_LIGHT


@pytest.mark.inventory
@pytest.mark.regression
class TestInventory:

    @pytest.mark.smoke
    def test_add_item_updates_cart_badge(self, logged_in_inventory_page: InventoryPage):
        """Adding one item to the cart bumps the cart badge count to 1."""
        logged_in_inventory_page.add_to_cart(BACKPACK)
        assert logged_in_inventory_page.get_cart_count() == 1

    def test_remove_item_updates_cart_badge(self, logged_in_inventory_page: InventoryPage):
        """Removing the only item in the cart brings the badge count back to 0."""
        logged_in_inventory_page.add_to_cart(BACKPACK)
        logged_in_inventory_page.remove_from_cart(BACKPACK)
        assert logged_in_inventory_page.get_cart_count() == 0

    def test_add_multiple_items_updates_cart_badge(self, logged_in_inventory_page: InventoryPage):
        """Adding two different items updates the cart badge count to 2."""
        logged_in_inventory_page.add_to_cart(BACKPACK)
        logged_in_inventory_page.add_to_cart(BIKE_LIGHT)
        assert logged_in_inventory_page.get_cart_count() == 2

    def test_sort_price_low_to_high(self, logged_in_inventory_page: InventoryPage):
        """The 'Price (low to high)' sort option orders products ascending by price."""
        logged_in_inventory_page.sort_by("lohi")
        prices = logged_in_inventory_page.get_item_prices()
        assert prices == sorted(prices)

    def test_sort_price_high_to_low(self, logged_in_inventory_page: InventoryPage):
        """The 'Price (high to low)' sort option orders products descending by price."""
        logged_in_inventory_page.sort_by("hilo")
        prices = logged_in_inventory_page.get_item_prices()
        assert prices == sorted(prices, reverse=True)

    def test_sort_name_a_to_z(self, logged_in_inventory_page: InventoryPage):
        """The 'Name (A to Z)' sort option orders products alphabetically."""
        logged_in_inventory_page.sort_by("az")
        names = logged_in_inventory_page.get_item_names()
        assert names == sorted(names)

    @pytest.mark.smoke
    def test_logout_returns_to_login_page(self, logged_in_inventory_page: InventoryPage):
        """Logging out from the inventory page returns the user to the login screen."""
        logged_in_inventory_page.logout()
        login_page = LoginPage(logged_in_inventory_page.page)
        assert login_page.is_visible(login_page.LOGIN_BUTTON)
