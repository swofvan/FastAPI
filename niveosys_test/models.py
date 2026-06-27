from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from datetime import datetime

from database import Base


class User(Base):

    __tablename__ = "Users"

    userid = Column(Integer, primary_key=True, index=True)

    fullname = Column(String(100))

    email = Column(String(100), unique=True)

    mobilenumber = Column(String(20), unique=True)

    password = Column(String(225))

    profileimage = Column(String(500))

    isactive = Column(Boolean, default=True)

    createdat = Column(DateTime, default=datetime.utcnow)

    updatedat = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )