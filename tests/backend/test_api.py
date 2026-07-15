from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"]
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_participant_and_rejects_duplicates(client):
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]

    duplicate_response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant(client):
    email = "michael@mergington.edu"

    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_not_found(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
