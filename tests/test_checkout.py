"""
Checkout flow test suite — the core end-to-end purchase journey.
Covers: full happy-path purchase and missing customer-info validation.
"""
import pytest
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage
from utils.sauce_data import BACKPACK, BIKE_LIGHT
from utils.test_data import random_first_name, random_last_name, random_zip_code


@pytest.mark.checkout
@pytest.mark.regression
class TestCheckout:

    @pytest.mark.smoke
    def test_complete_purchase_end_to_end(
        self,
        logged_in_inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_info_page: CheckoutInfoPage,
        checkout_overview_page: CheckoutOverviewPage,
        checkout_complete_page: CheckoutCompletePage,
    ):
        """Full happy-path purchase: add items, check out, fill info, confirm order."""
        logged_in_inventory_page.add_to_cart(BACKPACK)
        logged_in_inventory_page.add_to_cart(BIKE_LIGHT)
        logged_in_inventory_page.go_to_cart()

        cart_page.checkout()
        checkout_info_page.fill_info(random_first_name(), random_last_name(), random_zip_code())
        checkout_info_page.continue_checkout()

        checkout_overview_page.assert_url_contains("checkout-step-two.html")
        checkout_overview_page.finish()

        checkout_complete_page.assert_url_contains("checkout-complete.html")
        assert "Thank you for your order" in checkout_complete_page.get_confirmation_message()

    def test_checkout_requires_customer_info(
        self,
        logged_in_inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_info_page: CheckoutInfoPage,
    ):
        """Continuing checkout with no customer info shows a required-field error."""
        logged_in_inventory_page.add_to_cart(BACKPACK)
        logged_in_inventory_page.go_to_cart()
        cart_page.checkout()

        checkout_info_page.continue_checkout()  # no info filled in
        assert "First Name is required" in checkout_info_page.get_error_message()
