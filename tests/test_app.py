import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]
    # Remove
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate():
    activity = "Chess Club"
    email = "daniel@mergington.edu"  # già presente
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_nonexistent_participant():
    activity = "Chess Club"
    email = "nonexistent@mergington.edu"
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_nonexistent_activity():
    response = client.delete("/activities/NonexistentActivity/participant?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
