"""
Fixtures that instantiate Page Objects — keeps test files clean,
they just ask for 'login_page' etc. instead of building it themselves.
"""
import pytest
from playwright.sync_api import Page
from config.config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage
from utils.sauce_data import STANDARD_USER, PASSWORD


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_info_page(page: Page) -> CheckoutInfoPage:
    return CheckoutInfoPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)


@pytest.fixture
def logged_in_inventory_page(login_page: LoginPage) -> InventoryPage:
    """Logs in as the standard user and lands on the inventory page — used by
    cart/checkout tests that don't care about exercising the login flow itself."""
    login_page.open(Config.BASE_URL)
    login_page.login(STANDARD_USER, PASSWORD)
    return InventoryPage(login_page.page)
