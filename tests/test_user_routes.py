from app import database
from blueprints.excel import add_person


def test_get_by_name(app, client, valid_user, json_user):
    """
    test getting a user by a valid name after they have been added to the database
    :param: see conftest.py for all params
    """
    with app.test_request_context():
        add_person(valid_user)
        name = json_user["first_name"]
        response = client.get(f"/get/{name}")

        assert response.status_code == 200
        assert response.json["message"] == json_user


def test_get_wrong_name(app, client):
    """
    test that the application falls over correctly and returns a 404 for a user that doesn't exist.
    :param: see conftest.py for all params
    """
    name = "Random Name"
    with app.test_request_context():
        response = client.get(f"/get/{name}")

        assert response.status_code == 404
        assert response.json["error"] == f"User ({name}) not found."


def test_all_users(app, client, populate_database):
    """
    test that a database exists with multiple users and return them as json objects.
    :param: see conftest.py for all params
    """
    with app.test_request_context():
        response = client.get("/get/all")

        assert response.status_code == 200

        assert response.json["message"] == [
            {"date_of_birth": "Sat, 12 May 1956 00:00:00 GMT", "first_name": "Homer", "gender": "M",
             "last_name": "Simpson", "membership_no": 55555555555, "researcher": False, "time_in": "09:00:00",
             "valid_from": "Thu, 01 Jan 1970 00:00:00 GMT", "valid_to": "Tue, 19 Jan 2038 00:00:00 GMT"},
            {"date_of_birth": "Sun, 19 Apr 1987 00:00:00 GMT", "first_name": "Lisa", "gender": "F",
             "last_name": "Simpson", "membership_no": 66666666666, "researcher": True, "time_in": "09:00:00",
             "valid_from": "Mon, 01 Feb 1999 00:00:00 GMT", "valid_to": "Wed, 19 May 2038 00:00:00 GMT"},
            {"date_of_birth": "Sat, 19 Apr 1980 00:00:00 GMT", "first_name": "Bart", "gender": "M",
             "last_name": "Simpson", "membership_no": 77777777777, "researcher": False, "time_in": "09:00:00",
             "valid_from": "Sun, 01 Jan 1922 00:00:00 GMT", "valid_to": "Tue, 30 Apr 2024 00:00:00 GMT"}
        ]


def test_no_users(app, client):
    """
    test that no users exist in the database and return an appropriate error message
    :param: see conftest.py for all params
    """
    with app.test_request_context():
        # clean up databases by deleting and reacting them before running test, to ensure no users exist.
        database.drop_all()
        database.create_all()

        response = client.get("/get/all")

        assert response.status_code == 200
        assert response.json["message"] == "No users have been added."
