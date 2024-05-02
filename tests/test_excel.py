from app import database
from models.user import User


def test_no_excel_file(app, client, dummy_file_information):
    with app.test_request_context():

        file_name = dummy_file_information["bad_file_name"]
        request = client.post("/read", json={"file_path": f"{file_name}"})

        assert request.status_code == 404
        assert request.json["error"] == f"the file (static/{file_name}) doesn't exist."


def test_excel_read(app, client, dummy_file_information):
    with app.test_request_context():
        file_name = dummy_file_information["good_file_name"]
        print(file_name)
        request = client.post("/read", json={"file_path": f"{file_name}"}, content_type="application/json")
        print(request.data)

        assert request.status_code == 200

        total_users = database.session.query(User).count()

        assert total_users == 85

# def test_bad_xl_data(app, client):
#     pass
#     # given that I've got a path to XL
#     # when given bad data
#     # then assert that the data is bad, i.e. post request response
