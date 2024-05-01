from flask import Blueprint, jsonify
from models.user import User

users = Blueprint("users_blueprint", __name__)


@users.route("/get/<name>", methods=["GET"])
def get_user_by_name(name: str):
    """
    get a user's information by searching for their name in the database.
    :param name: the user's name to get from the database
    :return: (json) object of the requested user's information.
    """
    # improve by allowing for lowercase name search using 'like' instead of just exact case.
    # split the incoming request into first and last name
    full_name = name.split(" ")
    first_name = full_name[0]
    last_name = full_name[-1]

    user = User()

    # if both first and last name exist try querying the database for both.
    if first_name and last_name:
        user = User.query.filter_by(first_name=first_name, last_name=last_name).first()

    # ditto but only with first name
    if first_name:
        user = User.query.filter_by(first_name=first_name).first()

    # fall over check to see if the request only contains a last name, before returning 'user not found'
    if not user:
        user = User.query.filter_by(last_name=last_name).first()

    if user:
        return jsonify({"message": user.to_dict()}), 200
    else:
        return jsonify({"error": f"User ({name}) not found."}), 404


@users.route("/get/all", methods=["GET"])
def get_all_users():
    """
    get all users from the database.
    :return: (json) object of all users.
    """
    all_users = User.query.all()
    excel_data = []

    for user in all_users:
        excel_data.append(user.to_dict())

    if len(excel_data) == 0:
        return jsonify({"message": "No users have been added."}), 200
    else:
        return jsonify({"message": excel_data}), 200
