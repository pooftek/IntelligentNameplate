"""
test_student.py — Tests for the student nameplate interface.
"""
import pytest


def _api_post(page, url, data, headers=None):
    return page.evaluate(
        """async ([url, data, headers]) => {
        const h = Object.assign({'Content-Type': 'application/json'}, headers || {});
        const r = await fetch(url, {
            method: 'POST',
            headers: h,
            body: JSON.stringify(data)
        });
        return r.json();
    }""",
        [url, data, headers or {}],
    )


def test_student_page_loads(live_server, page):
    """The student nameplate entry page should load."""
    page.goto(f"{live_server}/student", wait_until="domcontentloaded")
    # Should show the dual-screen nameplate interface
    assert page.locator(".np-root").is_visible() or "student" in page.url.lower()


def test_student_login_with_valid_number(live_server, page, created_class, professor_page):
    """
    A student enrolled in a class should be able to log in via the student interface.
    We first create & enroll the student via the professor API, then log in as that student.
    """
    if not created_class:
        pytest.skip("No class available")

    professor_page.evaluate(
        """async ([classId]) => {
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
    }""",
        [created_class],
    )

    student_number = "987654321"

    page.goto(f"{live_server}/student", wait_until="domcontentloaded")
    page.wait_for_selector(".np-root", timeout=3000)

    result = _api_post(page, f"{live_server}/api/student/login", {"identifier": student_number})
    assert result.get("success") is True
    assert result.get("token")
    assert result.get("student")

    cur = page.evaluate(
        """async ([url, token]) => {
        const r = await fetch(url, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        return r.json();
    }""",
        [f"{live_server}/api/student/current", result["token"]],
    )
    assert cur.get("success") is True
    assert cur.get("student", {}).get("student_number") == student_number


def test_parallel_student_bearer_tokens_same_browser(live_server, created_class, professor_page):
    """
    One browser context = one Flask session cookie. After two logins, each Bearer token
    must still resolve to the correct student (fixes multi-tab / multi-student collision).
    """
    if not created_class:
        pytest.skip("No class available")

    def create_student(number, email, first="T", last="Student"):
        return professor_page.evaluate(
            """async ([classId, number, email, first, last]) => {
            const r = await fetch(`/api/create_and_add_student/${classId}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    first_name: first,
                    last_name: last,
                    student_number: number,
                    email: email
                })
            });
            return r.json();
        }""",
            [created_class, number, email, first, last],
        )

    assert create_student("111111111", "tab1@comet.test").get("success") is True
    assert create_student("222222222", "tab2@comet.test").get("success") is True

    pwd = "StudentPw99"
    out = professor_page.evaluate(
        """async ([base, pwd]) => {
        async function loginToken(student_number) {
            let lr = await fetch(base + '/api/student/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ identifier: student_number })
            });
            let ld = await lr.json();
            if (!ld.success) return { err: 'login', ld };
            let token = ld.token;
            if (ld.needs_password) {
                let sr = await fetch(base + '/api/student/set_password', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    body: JSON.stringify({ password: pwd, confirm_password: pwd })
                });
                let sd = await sr.json();
                if (!sd.success) return { err: 'set_password', sd };
                token = sd.token;
            }
            return { token };
        }
        const t1 = await loginToken('111111111');
        if (t1.err) return t1;
        const t2 = await loginToken('222222222');
        if (t2.err) return t2;
        const c1 = await fetch(base + '/api/student/current', {
            headers: { 'Authorization': 'Bearer ' + t1.token }
        });
        const c2 = await fetch(base + '/api/student/current', {
            headers: { 'Authorization': 'Bearer ' + t2.token }
        });
        const d1 = await c1.json();
        const d2 = await c2.json();
        return {
            id1: d1.student && d1.student.id,
            id2: d2.student && d2.student.id,
            n1: d1.student && d1.student.student_number,
            n2: d2.student && d2.student.student_number,
            ok1: d1.success,
            ok2: d2.success
        };
    }""",
        [live_server, pwd],
    )

    assert out.get("ok1") and out.get("ok2"), out
    assert out.get("n1") == "111111111" and out.get("n2") == "222222222", out
    assert out.get("id1") != out.get("id2"), out


def test_student_interface_has_interaction_buttons(live_server, page):
    """The student session screen should have hand raise and thumbs buttons."""
    page.goto(f"{live_server}/student", wait_until="domcontentloaded")
    content = page.content()
    # These buttons are in the DOM even if not visible yet
    assert "hand" in content.lower() or "raise" in content.lower()
    assert "thumb" in content.lower()
