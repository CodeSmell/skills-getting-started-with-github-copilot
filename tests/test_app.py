from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data



def test_signup_add_user():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_signup_duplicate_user():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure user is present
    client.post(f"/activities/{activity}/unregister?email={email}")
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_unregister_from_activity():
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Removed")
    # Try removing again (should fail)
    response2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 404
