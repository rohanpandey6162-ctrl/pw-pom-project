"""
Login test suite for SauceDemo.
Covers: successful login, locked-out user, and field-validation errors.
"""
import pytest
from config.config import Config
from pages.login_page import LoginPage
from utils.sauce_data import LOCKED_OUT_USER, PASSWORD, STANDARD_USER


@pytest.mark.login
class TestLogin:

    @pytest.mark.smoke
    def test_successful_login(self, login_page: LoginPage):
        """A valid standard_user/secret_sauce login lands on the inventory page."""
        login_page.open(Config.BASE_URL)
        login_page.login(STANDARD_USER, PASSWORD)
        login_page.wait_for_url("**/inventory.html")
        login_page.assert_url_contains("inventory.html")

    @pytest.mark.regression
    def test_locked_out_user_is_rejected(self, login_page: LoginPage):
        """A locked_out_user is blocked from logging in with a clear error message."""
        login_page.open(Config.BASE_URL)
        login_page.login(LOCKED_OUT_USER, PASSWORD)
        assert login_page.is_error_visible()
        assert "locked out" in login_page.get_error_message().lower()

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            ("", "", "Username is required"),
            (STANDARD_USER, "", "Password is required"),
            ("invalid_user", "wrong_password", "Username and password do not match"),
        ],
    )
    def test_login_validation_errors(
        self, login_page: LoginPage, username, password, expected_error
    ):
        """Missing/incorrect credentials each show their own specific validation error."""
        login_page.open(Config.BASE_URL)
        login_page.login(username, password)
        assert login_page.is_error_visible()
        assert expected_error in login_page.get_error_message()
