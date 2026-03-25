"""
conftest.py — Shared test fixtures for the Comet test suite.

What this file does:
- Starts a real Flask server on port 5001 before tests run
- Creates a temporary database so tests never touch production data
- Provides helper fixtures: a logged-in professor, an enrolled student
- Shuts the server down and cleans up after all tests finish
"""
import pytest
import subprocess
import uuid
from playwright.sync_api import TimeoutError as PlaywrightTimeout
import time
import os
import sys
import socket
import tempfile
import shutil

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Avoid 5000/5001 — often used by local dev and may be occupied by a hung or non-HTTP process.
TEST_PORT = int(os.environ.get("PYTEST_CLASSROOM_PORT", "18764"))
# Use 127.0.0.1 so Playwright and the Flask bind (0.0.0.0) agree on IPv4; "localhost" can prefer IPv6 (::1) on Windows.
BASE_URL = f"http://127.0.0.1:{TEST_PORT}"

TEST_PROFESSOR = {"username": "testprof", "email": "testprof@comet.test", "password": "TestPass123"}
TEST_CLASS = {"name": "Test Class 101", "code": "TC101"}
TEST_STUDENT = {
    "first_name": "Alice",
    "last_name": "Smith",
    "student_number": "123456789",
    "email": "alice@comet.test",
}


def wait_for_port(port, timeout=15):
    """Wait until the server is accepting connections."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            s = socket.create_connection(("127.0.0.1", port), timeout=1)
            s.close()
            return True
        except (ConnectionRefusedError, OSError):
            time.sleep(0.3)
    return False


@pytest.fixture(scope="session")
def tmp_db(tmp_path_factory):
    """Create a temporary directory to hold the test database."""
    return tmp_path_factory.mktemp("testdb")


@pytest.fixture(scope="session")
def live_server(tmp_db):
    """
    Start the Flask app as a subprocess on TEST_PORT with a fresh database.
    'scope=session' means it starts once and stays up for all tests.
    """
    db_path = str(tmp_db / "test_classroom_app.db")
    env = os.environ.copy()
    env["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    env["TESTING"] = "1"
    env["SECRET_KEY"] = "test-secret-key-not-for-production"
    env["PORT"] = str(TEST_PORT)

    proc = subprocess.Popen(
        [sys.executable, os.path.join(PROJECT_ROOT, "app.py")],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=PROJECT_ROOT,
    )

    if not wait_for_port(TEST_PORT):
        proc.terminate()
        pytest.fail(
            f"Flask server did not start on port {TEST_PORT}. "
            "Ensure nothing else is bound to that port and app.py starts with TESTING=1."
        )

    yield BASE_URL

    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


@pytest.fixture(scope="session")
def registered_professor(live_server, playwright):
    """Register a professor account once for the entire test session."""
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto(f"{live_server}/register", wait_until="domcontentloaded")

    page.fill("#username", TEST_PROFESSOR["username"])
    page.fill("#email", TEST_PROFESSOR["email"])
    page.fill("#password", TEST_PROFESSOR["password"])
    page.fill("#confirmPassword", TEST_PROFESSOR["password"])
    page.click("button[type=submit]")
    try:
        page.wait_for_url(f"{live_server}/dashboard", timeout=15000, wait_until='domcontentloaded')
    except PlaywrightTimeout:
        # Another test may have registered this user first (same session DB).
        page.goto(f"{live_server}/login", wait_until='domcontentloaded')
        page.fill("#username", TEST_PROFESSOR["username"])
        page.fill("#password", TEST_PROFESSOR["password"])
        page.click("button[type=submit]")
        page.wait_for_url(f"{live_server}/dashboard", timeout=15000, wait_until='domcontentloaded')
    browser.close()
    return TEST_PROFESSOR


@pytest.fixture
def professor_page(live_server, registered_professor, page):
    """
    Provide a Playwright page that is already logged in as a professor.
    'page' is a built-in Playwright fixture — a fresh browser tab per test.
    """
    page.goto(f"{live_server}/login", wait_until="domcontentloaded")
    page.fill("#username", registered_professor["username"])
    page.fill("#password", registered_professor["password"])
    page.click("button[type=submit]")
    page.wait_for_url(f"{live_server}/dashboard", timeout=15000, wait_until='domcontentloaded')
    return page


@pytest.fixture(scope="session")
def created_class(live_server, registered_professor, playwright):
    """Create a class once and return its URL for use in multiple tests."""
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Login
    page.goto(f"{live_server}/login", wait_until="domcontentloaded")
    page.fill("#username", registered_professor["username"])
    page.fill("#password", registered_professor["password"])
    page.click("button[type=submit]")
    page.wait_for_url(f"{live_server}/dashboard", timeout=15000, wait_until='domcontentloaded')

    # Create class via API (unique code avoids collisions if DB is reused or TC101 already exists)
    session_code = "TC" + uuid.uuid4().hex[:6].upper()
    response = page.evaluate("""async ([name, class_code]) => {
        const r = await fetch('/api/create_class', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, class_code})
        });
        return r.json();
    }""", [TEST_CLASS["name"], session_code])

    browser.close()
    cid = response.get("class_id")
    if not cid:
        pytest.fail(f"Session fixture create_class failed: {response!r}")
    return cid
