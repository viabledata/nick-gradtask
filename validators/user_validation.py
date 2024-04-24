from pydantic import BaseModel, field_validator, field_serializer, ValidationError
from datetime import date, datetime, time


class UserValidation(BaseModel):
    name: str
    date_of_birth: date | str
    time_in: time
    membership_no: int
    valid_from: datetime
    valid_to: datetime | str
    gender: str
    researcher: bool

    @field_validator('date_of_birth')
    @classmethod
    def validate_dob(cls, date_of_birth):
        """
        validate incoming date of births and update them into a 'new_date' format,
        if the incoming date is a string.
        :param date_of_birth: the date of birth to be checked
        :return: either a new date object, or valid date of birth
        """
        if isinstance(date_of_birth, str):
            date_format = '%d/%m/%Y'
            new_date = datetime.strptime(date_of_birth, date_format).date()
            return new_date
        else:
            return date_of_birth

    @field_validator('name')
    @classmethod
    def split_and_validate_name(cls, full_name: str) -> dict:
        """
        Validate and split names into first & last, trim whitespace and excess spaces in names,
        including numbers and special characters.
        :param full_name: the full name to be split and trimmed
        :return: dict of firstname and last name.
        """
        num_check = any(character.isdigit() for character in full_name)

        if num_check:
            raise ValueError(f"This name contains a number: {full_name}")

        print("Current name:", full_name)
        full_name.strip()
        full_name.replace(" ", "")

        formatted_name = " ".join(full_name.split())
        split_name = formatted_name.split(" ")

        return {"first_name": split_name[0], "last_name": split_name[1]}

    @field_serializer('researcher')
    @classmethod
    def serialize_researcher(cls, value):
        """
        Convert researcher from 'yes / no' value to boolean true/false
        :param value: the type of researcher to be changed
        :return: either true or false depending on if the person is a researcher
        """
        if value.lower() == 'y' or value.lower() == 'yes':
            return True
        else:
            return False