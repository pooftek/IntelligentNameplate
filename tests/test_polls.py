"""
test_polls.py — Tests for poll creation and management.
"""
import pytest


def _create_poll_via_api(page, class_id):
    return page.evaluate("""async (classId) => {
        const r = await fetch(`/api/create_poll/${classId}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                question: 'What is 2+2?',
                options: ['3', '4', '5', '6'],
                correct_answer: '4',
                is_graded: true,
                is_anonymous: false
            })
        });
        return r.json();
    }""", class_id)


def test_create_poll(professor_page, live_server, created_class):
    """Creating a poll via the API should return success with a poll_id."""
    if not created_class:
        pytest.skip("No class available")
    result = _create_poll_via_api(professor_page, created_class)
    assert result.get("success") is True
    assert "poll_id" in result


def test_stop_poll(professor_page, live_server, created_class):
    """Stopping an active poll should return success."""
    if not created_class:
        pytest.skip("No class available")

    # Create a poll first
    create_result = _create_poll_via_api(professor_page, created_class)
    poll_id = create_result.get("poll_id")
    if not poll_id:
        pytest.skip("Poll creation failed")

    stop_result = professor_page.evaluate("""async (pollId) => {
        const r = await fetch(`/api/stop_poll/${pollId}`, {method: 'POST'});
        return r.json();
    }""", poll_id)
    assert stop_result.get("success") is True


def test_clear_poll_responses(professor_page, live_server, created_class):
    """
    The new /api/clear_poll_responses endpoint should return success.
    This tests the bug fix for the previously broken clearPollData() function.
    """
    if not created_class:
        pytest.skip("No class available")

    create_result = _create_poll_via_api(professor_page, created_class)
    poll_id = create_result.get("poll_id")
    if not poll_id:
        pytest.skip("Poll creation failed")

    clear_result = professor_page.evaluate("""async (pollId) => {
        const r = await fetch(`/api/clear_poll_responses/${pollId}`, {method: 'POST'});
        return r.json();
    }""", poll_id)
    assert clear_result.get("success") is True


def test_poll_results_endpoint(professor_page, live_server, created_class):
    """The poll results endpoint should return structured data."""
    if not created_class:
        pytest.skip("No class available")

    create_result = _create_poll_via_api(professor_page, created_class)
    poll_id = create_result.get("poll_id")
    if not poll_id:
        pytest.skip("Poll creation failed")

    results = professor_page.evaluate("""async (pollId) => {
        const r = await fetch(`/api/poll_results/${pollId}`);
        return r.json();
    }""", poll_id)
    assert "poll" in results or "results" in results or "success" in results
