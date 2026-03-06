from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_and_unregister_cycle():
    # Arrange: Ensure starting state does not contain test user
    data = client.get("/activities").json()
    assert "testuser@school.edu" not in data["Chess Club"]["participants"]

    # Act: Sign up should succeed
    res = client.post("/activities/Chess%20Club/signup?email=testuser@school.edu")

    # Assert
    assert res.status_code == 200
    assert "Signed up testuser@school.edu" in res.json().get("message", "")

    # Arrange: (test user is now signed up)

    # Act: Duplicate sign-up should be rejected
    res = client.post("/activities/Chess%20Club/signup?email=testuser@school.edu")

    # Assert
    assert res.status_code == 400
    assert res.json().get("detail") == "Student already signed up for this activity"

    # Arrange: (test user is signed up)

    # Act: Unregister should succeed
    res = client.delete("/activities/Chess%20Club/participants?email=testuser@school.edu")

    # Assert
    assert res.status_code == 200
    assert "Unregistered testuser@school.edu" in res.json().get("message", "")

    # Arrange: (test user is now unregistered)

    # Act: Unregister again should 404
    res = client.delete("/activities/Chess%20Club/participants?email=testuser@school.edu")

    # Assert
    assert res.status_code == 404
    assert res.json().get("detail") == "Student not registered"


def test_activity_endpoints_errors_and_listing():
    """Test activity endpoints with error handling using AAA pattern."""
    # Arrange
    activity_name = "Chess Club"

    # Act
    data = client.get("/activities").json()

    # Assert: Get activities list returns top-level dict
    assert isinstance(data, dict)
    assert activity_name in data

    # Arrange
    non_existent_activity = "NoSuch"
    test_email = "foo@bar.com"

    # Act: Signup to non-existent activity
    res = client.post(f"/activities/{non_existent_activity}/signup?email={test_email}")

    # Assert: Should 404
    assert res.status_code == 404

    # Act: Unregister from non-existent activity
    res = client.delete(f"/activities/{non_existent_activity}/participants?email={test_email}")

    # Assert: Should 404
    assert res.status_code == 404
