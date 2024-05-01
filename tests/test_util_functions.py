from blueprints.excel import add_person, validate_data
from models.user import User


def test_validate_data(app, list_user, valid_user):
    with app.test_request_context():
        assert validate_data(list_user) == valid_user


def test_add_person(app, valid_user):
    with app.test_request_context():
        add_person(valid_user)
        user_query = User.query.filter_by(first_name=valid_user.name["first_name"]).first()
    assert user_query.membership_no == valid_user.membership_no
