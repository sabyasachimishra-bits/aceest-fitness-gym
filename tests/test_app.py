import pytest

from app import create_app


@pytest.fixture()
def app():
    application = create_app()
    application.config.update({"TESTING": True})
    return application


@pytest.fixture()
def client(app):
    return app.test_client()


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()
    assert data["application"] == "ACEest Fitness & Gym"
    assert data["status"] == "running"


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_get_all_workouts(client):
    response = client.get("/workouts")

    assert response.status_code == 200

    data = response.get_json()
    assert data["count"] == 2
    assert len(data["workouts"]) == 2


def test_get_existing_workout(client):
    response = client.get("/workouts/1")

    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Push Ups"


def test_get_non_existing_workout(client):
    response = client.get("/workouts/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Workout not found"


def test_add_workout_successfully(client):
    workout = {
        "name": "Cycling",
        "category": "Cardio",
        "duration_minutes": 45,
    }

    response = client.post("/workouts", json=workout)

    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Cycling"
    assert data["duration_minutes"] == 45
    assert "id" in data


def test_add_workout_with_missing_field(client):
    workout = {
        "name": "Cycling",
        "category": "Cardio",
    }

    response = client.post("/workouts", json=workout)

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Missing required fields"
    assert "duration_minutes" in data["missing_fields"]


def test_add_workout_with_invalid_duration(client):
    workout = {
        "name": "Cycling",
        "category": "Cardio",
        "duration_minutes": -10,
    }

    response = client.post("/workouts", json=workout)

    assert response.status_code == 400
    assert "positive integer" in response.get_json()["error"]


def test_calorie_calculation(client):
    request_data = {
        "duration_minutes": 30,
        "calories_per_minute": 8,
    }

    response = client.post("/calories", json=request_data)

    assert response.status_code == 200
    assert response.get_json()["total_calories"] == 240


def test_calorie_calculation_with_invalid_duration(client):
    request_data = {
        "duration_minutes": 0,
        "calories_per_minute": 8,
    }

    response = client.post("/calories", json=request_data)

    assert response.status_code == 400
    assert "positive number" in response.get_json()["error"]


def test_unknown_endpoint(client):
    response = client.get("/unknown")

    assert response.status_code == 404