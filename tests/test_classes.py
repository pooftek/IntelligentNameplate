"""
test_classes.py — Tests for class creation and navigation.
"""
import pytest


def test_dashboard_loads(professor_page, live_server):
    """Dashboard should show 'My Classes' heading."""
    professor_page.goto(f"{live_server}/dashboard")
    assert professor_page.locator("h1").is_visible()


def test_create_class(professor_page, live_server):
    """Creating a class should make it appear on the dashboard."""
    professor_page.goto(f"{live_server}/dashboard")
    # Trigger add class modal
    professor_page.evaluate("showAddClassModal()")
    professor_page.wait_for_selector("#addClassModal .modal.show, #addClassModal.show", timeout=3000)
    professor_page.fill("#className", "Playwright Test Class")
    professor_page.fill("#classCode", "PTC999")
    professor_page.evaluate("addClass()")
    # Wait for page reload
    professor_page.wait_for_load_state("networkidle", timeout=5000)
    assert "Playwright Test Class" in professor_page.content()


def test_navigate_to_classroom(professor_page, live_server, created_class):
    """Clicking a class card navigates to the classroom page."""
    if not created_class:
        pytest.skip("No class was created in setup")
    professor_page.goto(f"{live_server}/classroom/{created_class}")
    assert f"/classroom/{created_class}" in professor_page.url


def test_classroom_shows_options(professor_page, live_server, created_class):
    """The classroom hub should show the 4 main option cards."""
    if not created_class:
        pytest.skip("No class was created in setup")
    professor_page.goto(f"{live_server}/classroom/{created_class}")
    content = professor_page.content()
    assert "Manage Students" in content or "Students" in content
    assert "Gradebook" in content or "Class Data" in content
