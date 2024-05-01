import re, random

from dateutil import parser
from pydantic import BaseModel, field_validator, field_serializer
from datetime import date, datetime, time

from models.user import User


class UserValidation(BaseModel):
    name: str
    date_of_birth: date | str
    time_in: time
    membership_no: int
    valid_from: datetime | str
    valid_to: datetime | str
    gender: str
    researcher: bool

    @field_validator('name')
    @classmethod
    def split_and_validate_name(cls, full_name: str) -> dict:
        """
        Validate and split names into first & last, trim whitespace, excess spaces in names,
        numbers and special characters.
        :param full_name: (str) the full name to be split and trimmed
        :return: (dict) of firstname and last name.
        """
        # Regex pattern to match numbers & special characters
        pattern = r"[0-9]|[,@(){}&*%$£!-+'\"/\\]|[/\[\]]"
        trimmed_name = re.sub(pattern, "", full_name)

        # strip any whitespace from beginning or end
        trimmed_name.strip()
        trimmed_name.replace(" ", "")

        # reformat the name with once space between first and last
        formatted_name = " ".join(trimmed_name.split())
        split_name = formatted_name.split(" ")

        return {"first_name": split_name[0], "last_name": split_name[1]}

    @field_validator('date_of_birth', 'valid_from', 'valid_to')
    @classmethod
    def validate_dates(cls, incoming_date) -> datetime:
        """
        validate incoming date/datetime formats and parses them with dateutil.
        :param incoming_date: the date to be checked
        :return: (datetime) either a new date object, or valid date of birth
        """
        # Check if the date is a string
        if isinstance(incoming_date, str):
            try:
                # try to parse and return the date
                parsed_date = parser.parse(incoming_date)
                return parsed_date
            except ValueError:
                raise ValueError(f"Invalid date format, {type(incoming_date)} expected: Str, Date, Datetime")
        else:
            return incoming_date

    @field_validator('time_in')
    @classmethod
    def validate_time_in(cls, time_in: time) -> time:
        """
        check if the incoming date matches hours and minutes format.
        :param time_in: (time)
        :return: (time) the incoming time or a new H:M time object.
        """
        # check if the incoming time is a string
        if isinstance(time_in, str):
            # create a new time in h:m format
            date_format = '%H:%M'
            new_time = datetime.strptime(time_in, date_format).time()
            return new_time
        else:
            return time_in

    @field_validator("membership_no")
    @classmethod
    def validate_membership_no(cls, membership_no: int) -> int:
        """
        validate the membership number, by checking the database if the membership number exists.
        :param membership_no: incoming membership number
        :return: (int) either the membership number or a newly generated one.
        """
        membership_query = User.query.filter_by(membership_no=membership_no).first()

        # if the membership_query already exists, generate a new one
        if membership_query:
            return cls.generate_membership_number()
        else:
            return membership_no

    @classmethod
    def generate_membership_number(cls) -> int:
        """
        recursive function to generate a new 6 digit membership_id
        :return: (int) new membership number
        """
        new_membership_no = random.randint(100000, 999999)
        new_membership_check = User.query.filter_by(membership_no=new_membership_no).first()

        if not new_membership_check:
            return new_membership_no
        else:
            return cls.generate_member_id()

    @field_serializer("gender")
    @classmethod
    def serialize_gender(cls, value: str) -> str:
        """
        Serialize the gender of a user by ensuring that it is either U, F, M.
        :param value: incoming gender string
        :return: (str) a single character of U,F,M in uppercase.
        """
        accepted_gender_letter = ["u", "f", "m"]
        accepted_gender_words = ["unknown", "female", "male"]

        if value.lower() in accepted_gender_letter:
            return value.upper()
        elif value.lower() in accepted_gender_words:
            return value[0].upper()
        else:
            raise ValueError(f"{value} is not a valid gender - expected: Male, Female, Unknown or U, F, M")

    @field_serializer("researcher")
    @classmethod
    def serialize_researcher(cls, value: str) -> bool:
        """
        Convert researcher from 'yes / no' value to boolean true/false
        :param value: the type of researcher to be changed
        :return: (boolean) either true or false depending on if the person is a researcher
        """
        if value.lower() == "y" or value.lower() == "yes":
            return True
        else:
            return False
