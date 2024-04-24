from validators.user_validation import UserValidation
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from openpyxl import load_workbook


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy()
database.init_app(app)

from models.user import User

with app.app_context():
    print(database.engine)
    database.create_all()


@app.route('/read', methods=["POST"])
def read_xl_file():
    """

    :return:
    """
    library_register = load_workbook("static/Library_register_data.xlsx")
    sheet = library_register.active

    # improve this file handling because dumping a larger file into memory... will not be ideal

    for row in range(2, sheet.max_row + 1):
        row_info = []
        for column in range(1, sheet.max_column + 1):

            cell = sheet.cell(row=row, column=column)
            if cell.value is not None:

                # column_name = sheet.cell(row=1, column=column)
                # print(f"Type: {type(cell.value)} {column_name.value}: {cell.value} |", end=" ")
                row_info.append(cell.value)

        # check if the row has data
        if row_info:
            add_person(validate_data(row_info))
            # debug print
            # print(f"Row to Dict: {validate_data(row_info)}")
            # print("-----------")

    users = User.query.all()
    excel_data = []

    for user in users:
        excel_data.append(user.to_dict())

    return jsonify({"message": excel_data})


def add_person(person):
    new_user = User(
        first_name=person.name["first_name"],
        last_name=person.name["last_name"],
        date_of_birth=person.date_of_birth,
    )

    database.session.add(new_user)
    database.session.commit()


def validate_data(row) -> UserValidation:
    """

    :param row:
    :return:
    """
    user = UserValidation(
        name=row[0],
        date_of_birth=row[1],
        time_in=row[2],
        membership_no=row[3],
        valid_from=row[4],
        valid_to=row[5],
        gender=row[6],
        researcher=row[7],
    )

    user.model_validate(user)

    print(user)

    # "time_in": str(user.time_in),
    # "membership_no": user.membership_no,
    # "valid_from": str(user.valid_from),
    # "valid_to": str(user.valid_to),
    # "gender": user.gender,
    # "researcher": user.researcher,

    return user


def load_file() -> str:
    """

    :return:
    """
    pass


if __name__ == '__main__':
    app.run()
