"""
test_gradebook.py — Tests for gradebook and class data page.
"""
import pytest


def test_class_data_page_loads(professor_page, live_server, created_class):
    """The class data/gradebook page should load."""
    if not created_class:
        pytest.skip("No class available")
    professor_page.goto(f"{live_server}/classroom/{created_class}/class_data")
    assert professor_page.locator("body").is_visible()
    assert professor_page.title() != ""


def test_gradebook_tab_visible(professor_page, live_server, created_class):
    """The Gradebook tab should be present on the class data page."""
    if not created_class:
        pytest.skip("No class available")
    professor_page.goto(f"{live_server}/classroom/{created_class}/class_data")
    content = professor_page.content()
    assert "gradebook" in content.lower() or "grade" in content.lower()


def test_preferences_api_saves_and_loads(professor_page, live_server):
    """
    The /api/preferences endpoint should save and return preferences.
    This tests the bug fix for the previously stubbed-out preferences endpoint.
    """
    # Save preferences
    save_result = professor_page.evaluate("""async () => {
        const r = await fetch('/api/preferences', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({show_first_name_only: true, quiet_mode: false})
        });
        return r.json();
    }""")
    assert save_result.get("success") is True

    # Load preferences back
    load_result = professor_page.evaluate("""async () => {
        const r = await fetch('/api/preferences');
        return r.json();
    }""")
    assert load_result.get("success") is True
    assert load_result.get("show_first_name_only") is True
    assert load_result.get("quiet_mode") is False
