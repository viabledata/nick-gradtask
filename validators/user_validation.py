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

    @field_validator('name')
    @classmethod
    def validate_name(cls, full_name: str):
        formatted_name = full_name.split(" ")

        print(formatted_name)

        return {"first_name": formatted_name[0], "last_name": formatted_name[1]}

    @field_validator('date_of_birth')
    @classmethod
    def validate_dob(cls, date_of_birth):
        if isinstance(date_of_birth, str):
            date_format = '%d/%m/%Y'
            new_date = datetime.strptime(date_of_birth, date_format).date()
            return new_date
        else:
            return date_of_birth

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