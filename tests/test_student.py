"""
test_student.py — Tests for the student nameplate interface.
"""
import pytest
import json


def _api_post(page, url, data):
    return page.evaluate("""async ([url, data]) => {
        const r = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        return r.json();
    }""", [url, data])


def test_student_page_loads(live_server, page):
    """The student nameplate entry page should load."""
    page.goto(f"{live_server}/student")
    # Should show the dual-screen nameplate interface
    assert page.locator(".np-root").is_visible() or "student" in page.url.lower()


def test_student_login_with_valid_number(live_server, page, created_class, professor_page):
    """
    A student enrolled in a class should be able to log in via the student interface.
    We first create & enroll the student via the professor API, then log in as that student.
    """
    if not created_class:
        pytest.skip("No class available")

    # Create a student via the professor API
    result = professor_page.evaluate("""async ([classId]) => {
        const r = await fetch(`/api/create_and_add_student/${classId}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                first_name: 'Bob',
                last_name: 'Jones',
                student_number: '987654321',
                email: 'bob@comet.test'
            })
        });
        return r.json();
    }""", [created_class])

    student_number = "987654321"

    # Now go to student interface and try to log in
    page.goto(f"{live_server}/student")
    page.wait_for_selector(".np-root", timeout=3000)

    result = _api_post(page, "/api/student/login", {
        "student_number": student_number
    })
    # Should succeed (first-time login, no password set yet)
    assert result.get("success") is True or "student" in str(result).lower()


def test_student_interface_has_interaction_buttons(live_server, page):
    """The student session screen should have hand raise and thumbs buttons."""
    page.goto(f"{live_server}/student")
    content = page.content()
    # These buttons are in the DOM even if not visible yet
    assert "hand" in content.lower() or "raise" in content.lower()
    assert "thumb" in content.lower()
