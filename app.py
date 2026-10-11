from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    workouts = [
        {
            "id": 1,
            "name": "Push Ups",
            "category": "Strength",
            "duration_minutes": 15,
        },
        {
            "id": 2,
            "name": "Running",
            "category": "Cardio",
            "duration_minutes": 30,
        },
    ]

    @app.get("/")
    def home():
        return jsonify(
            {
                "application": "ACEest Fitness & Gym",
                "message": "Welcome to the ACEest Fitness & Gym API",
                "status": "running",
            }
        )

    @app.get("/health")
    def health():
        return jsonify({"status": "healthy"}), 200

    @app.get("/workouts")
    def get_workouts():
        return jsonify({"count": len(workouts), "workouts": workouts}), 200

    @app.get("/workouts/<int:workout_id>")
    def get_workout(workout_id):
        workout = next(
            (item for item in workouts if item["id"] == workout_id),
            None,
        )

        if workout is None:
            return jsonify({"error": "Workout not found"}), 404

        return jsonify(workout), 200

    @app.post("/workouts")
    def add_workout():
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "JSON request body is required"}), 400

        required_fields = ["name", "category", "duration_minutes"]
        missing_fields = [
            field for field in required_fields if field not in data
        ]

        if missing_fields:
            return (
                jsonify(
                    {
                        "error": "Missing required fields",
                        "missing_fields": missing_fields,
                    }
                ),
                400,
            )

        if (
            not isinstance(data["duration_minutes"], int)
            or data["duration_minutes"] <= 0
        ):
            return (
                jsonify(
                    {
                        "error": (
                            "duration_minutes must be a positive integer"
                        )
                    }
                ),
                400,
            )

        new_workout = {
            "id": len(workouts) + 1,
            "name": data["name"],
            "category": data["category"],
            "duration_minutes": data["duration_minutes"],
        }

        workouts.append(new_workout)
        return jsonify(new_workout), 201

    @app.post("/calories")
    def calculate_calories():
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "JSON request body is required"}), 400

        duration = data.get("duration_minutes")
        calories_per_minute = data.get("calories_per_minute")

        if not isinstance(duration, (int, float)) or duration <= 0:
            return (
                jsonify(
                    {
                        "error": (
                            "duration_minutes must be a positive number"
                        )
                    }
                ),
                400,
            )

        if (
            not isinstance(calories_per_minute, (int, float))
            or calories_per_minute <= 0
        ):
            return (
                jsonify(
                    {
                        "error": (
                            "calories_per_minute must be a positive number"
                        )
                    }
                ),
                400,
            )

        total_calories = round(duration * calories_per_minute, 2)

        return (
            jsonify(
                {
                    "duration_minutes": duration,
                    "calories_per_minute": calories_per_minute,
                    "total_calories": total_calories,
                }
            ),
            200,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)