from app import database
from sqlalchemy import Column, String, Boolean, Integer, Date, DateTime, Time


class User(database.Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)

    date_of_birth = Column(Date, nullable=False)
    time_in = Column(Time, nullable=True)

    membership_no = Column(Integer, unique=True)

    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)

    gender = Column(String(1), nullable=True)
    researcher = Column(Boolean, nullable=True)

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'time_in': self.time_in,
            'membership_no': self.membership_no,
            'valid_from': self.valid_from,
            'valid_to': self.valid_to,
            'gender': self.gender,
            'researcher': self.researcher,
        }
