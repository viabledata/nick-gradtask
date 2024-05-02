import pytest
from datetime import datetime

from flask import Flask
from flask.testing import FlaskClient
from app import create_app, database
from config import TestConfig

from models.user import User
from validators.user_validation import UserValidation

from blueprints.users import get_all_users, get_user_by_name
from blueprints.excel import read_xl_file


@pytest.fixture(scope="session", autouse=True)
def app() -> Flask:
    """
    Create an App instance with rules from app.py
    """
    app = create_app(config_class=TestConfig)
    app.config.update({
        "TESTING": True
    })

    app.add_url_rule(rule="/get/all", view_func=get_all_users)
    app.add_url_rule(rule="/get/<name>", view_func=get_user_by_name)
    app.add_url_rule(rule="/read", view_func=read_xl_file)

    yield app


@pytest.fixture(scope="session", autouse=True)
def client(app) -> FlaskClient:
    """
    Return a Flask test client to run tests against.
    :param app: The app instance
    """
    return app.test_client()


@pytest.fixture(scope="module")
def populate_database(app):
    """Populate the database with simpsons data"""
    with app.test_request_context():

        database.drop_all()
        database.create_all()

        person_1 = User(
            first_name="Homer",
            last_name="Simpson",
            date_of_birth=datetime.strptime("12/05/1956", "%d/%m/%Y").date(),
            time_in=datetime.strptime("09:00", "%H:%M").time(),
            membership_no=55555555555,
            valid_from=datetime.strptime("01-01-1970 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
            valid_to=datetime.strptime("19-01-2038 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
            gender="M",
            researcher=False,
        )

        person_2 = User(
                first_name="Lisa",
                last_name="Simpson",
                date_of_birth=datetime.strptime("19/04/1987", "%d/%m/%Y").date(),
                time_in=datetime.strptime("09:00", "%H:%M").time(),
                membership_no=66666666666,
                valid_from=datetime.strptime("01-02-1999 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
                valid_to=datetime.strptime("19-05-2038 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
                gender="F",
                researcher=True,
            )

        person_3 = User(
                first_name="Bart",
                last_name="Simpson",
                date_of_birth=datetime.strptime("19/04/1980", "%d/%m/%Y").date(),
                time_in=datetime.strptime("09:00", "%H:%M").time(),
                membership_no=77777777777,
                valid_from=datetime.strptime("01-01-1922 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
                valid_to=datetime.strptime("30-04-2024 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
                gender="M",
                researcher=False,
            )

        database.session.add_all([person_1, person_2, person_3])
        database.session.commit()


@pytest.fixture(scope="module")
def list_user() -> list:
    """
    create a 'list user' (how a user should be before being passed into pydantic)
    :return:
    """
    time_in = datetime.strptime("09:28", "%H:%M").time()
    valid_from = datetime.strptime("27-02-2021 00:00:00", "%d-%m-%Y %H:%M:%S").date()
    valid_to = datetime.strptime("10-01-2020 00:00:00", "%d-%m-%Y %H:%M:%S").date()
    return ["Ned Flanders", "01/01/1950", time_in, 19500101, valid_from, valid_to, "M", True]


@pytest.fixture(scope="module")
def valid_user(app) -> UserValidation:
    """
    Return a validated user, after they've been parsed by pydantic
    """
    with app.test_request_context():
        return UserValidation(
            name="Ned Flanders",
            date_of_birth="01/01/1950",
            time_in=datetime.strptime("09:28", "%H:%M").time(),
            membership_no=19500101,
            valid_from=datetime.strptime("27-02-2021 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
            valid_to=datetime.strptime("10-01-2020 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
            gender='M',
            researcher=True
        )


@pytest.fixture(scope="module")
def database_user(app) -> User:
    """
    return a database User
    """
    with app.test_request_context():
        return User(
            first_name="Ned",
            last_name="Flanders",
            date_of_birth="01/01/1950",
            time_in=datetime.strptime("09:28", "%H:%M").time(),
            membership_no=19500101,
            valid_from=datetime.strptime("27-02-2021 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
            valid_to=datetime.strptime("10-01-2020 00:00:00", "%d-%m-%Y %H:%M:%S").date(),
            gender='M',
            researcher=True
        )


@pytest.fixture(scope="module")
def json_user() -> dict:
    return {
        "first_name": "Ned", "last_name": "Flanders", "date_of_birth": "Sun, 01 Jan 1950 00:00:00 GMT",
        "gender": "M", "membership_no": 19500101, "researcher": True, "time_in": "09:28:00",
        "valid_from": "Sat, 27 Feb 2021 00:00:00 GMT", "valid_to": "Fri, 10 Jan 2020 00:00:00 GMT"
    }


@pytest.fixture(scope="module")
def dummy_file_information() -> dict:
    return {
        "good_file_name": "data/Library_register_data.xlsx",
        "bad_file_name": "no_data_in_here.xlsx",
        "file_size": 1000,
        "amount_of_rows": 80,
        "file_format": ".xlsx"
    }