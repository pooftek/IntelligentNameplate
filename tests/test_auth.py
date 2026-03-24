"""
test_auth.py — Tests for professor login, register, and logout.

Each test opens a real browser and goes through the actual UI —
exactly like a user would. If something breaks (wrong redirect,
missing error message, etc.) the test fails and tells you what went wrong.
"""
import pytest


def test_login_page_loads(live_server, page):
    """The login page should show the Comet wordmark and a login form."""
    page.goto(f"{live_server}/login")
    assert page.locator(".comet-wordmark").is_visible()
    assert page.locator("#username").is_visible()
    assert page.locator("#password").is_visible()


def test_register_new_professor(live_server, page):
    """A new professor can register and gets sent to the dashboard."""
    page.goto(f"{live_server}/register")
    page.fill("#username", "newprof_test")
    page.fill("#email", "newprof@comet.test")
    page.fill("#password", "SecurePass123")
    page.fill("#confirmPassword", "SecurePass123")
    page.click("button[type=submit]")
    page.wait_for_url(f"{live_server}/dashboard", timeout=5000)
    assert "/dashboard" in page.url


def test_register_duplicate_username(live_server, registered_professor, page):
    """Registering with an existing username should show an error."""
    page.goto(f"{live_server}/register")
    page.fill("#username", registered_professor["username"])
    page.fill("#email", "other@comet.test")
    page.fill("#password", "SecurePass123")
    page.fill("#confirmPassword", "SecurePass123")
    page.click("button[type=submit]")
    # Should stay on register page and show an error
    page.wait_for_selector("#errorMessage:visible", timeout=3000)
    assert page.locator("#errorMessage").is_visible()


def test_register_password_mismatch(live_server, page):
    """Mismatched passwords should show a client-side error."""
    page.goto(f"{live_server}/register")
    page.fill("#username", "anothernewprof")
    page.fill("#email", "another@comet.test")
    page.fill("#password", "password1")
    page.fill("#confirmPassword", "password2")
    page.click("button[type=submit]")
    page.wait_for_selector("#errorMessage:visible", timeout=3000)
    assert "do not match" in page.locator("#errorMessage").inner_text().lower()


def test_login_valid_credentials(live_server, registered_professor, page):
    """Login with correct credentials redirects to dashboard."""
    page.goto(f"{live_server}/login")
    page.fill("#username", registered_professor["username"])
    page.fill("#password", registered_professor["password"])
    page.click("button[type=submit]")
    page.wait_for_url(f"{live_server}/dashboard", timeout=5000)
    assert "/dashboard" in page.url


def test_login_invalid_password(live_server, registered_professor, page):
    """Login with wrong password should show an error message."""
    page.goto(f"{live_server}/login")
    page.fill("#username", registered_professor["username"])
    page.fill("#password", "wrongpassword")
    page.click("button[type=submit]")
    page.wait_for_selector("#errorMessage:visible", timeout=3000)
    assert page.locator("#errorMessage").is_visible()


def test_logout(live_server, professor_page):
    """Logging out redirects to the login page."""
    professor_page.goto(f"{live_server}/logout")
    professor_page.wait_for_url(f"{live_server}/login", timeout=5000)
    assert "/login" in professor_page.url


def test_protected_route_redirects_when_not_logged_in(live_server, page):
    """Visiting /dashboard without being logged in should redirect to login."""
    page.goto(f"{live_server}/dashboard")
    page.wait_for_url("**/login**", timeout=5000)
    assert "login" in page.url
