from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_and_unregister_cycle():
    # ensure starting state does not contain test user
    data = client.get("/activities").json()
    assert "testuser@school.edu" not in data["Chess Club"]["participants"]

    # sign up should succeed
    res = client.post("/activities/Chess%20Club/signup?email=testuser@school.edu")
    assert res.status_code == 200
    assert "Signed up testuser@school.edu" in res.json().get("message", "")

    # duplicate sign-up should be rejected
    res = client.post("/activities/Chess%20Club/signup?email=testuser@school.edu")
    assert res.status_code == 400
    assert res.json().get("detail") == "Student already signed up for this activity"

    # unregister should succeed
    res = client.delete("/activities/Chess%20Club/participants?email=testuser@school.edu")
    assert res.status_code == 200
    assert "Unregistered testuser@school.edu" in res.json().get("message", "")

    # unregister again should 404
    res = client.delete("/activities/Chess%20Club/participants?email=testuser@school.edu")
    assert res.status_code == 404
    assert res.json().get("detail") == "Student not registered"
