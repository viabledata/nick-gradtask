from flask import Blueprint, jsonify
from sqlalchemy import func

from models.user import User

users = Blueprint("users_blueprint", __name__)


@users.route("/users/<name>", methods=["GET"])
def get_user_by_name(name: str):
    """
    get a user's information by searching for their name in the database.
    :param name: the user's name to get from the database
    :return: (json) object of the requested user's information.
    """
    # improve by allowing for lowercase name search using 'like' instead of just exact case.
    # split the incoming request into first and last name

    user = User.query.filter(func.lower(User.first_name + ' ' + User.last_name).like(f"%{name.lower()}%")).first()

    if user:
        return jsonify({"message": user.to_dict()}), 200
    else:
        return jsonify({"error": f"User ({name}) not found."}), 404


@users.route("/users", methods=["GET"])
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
