from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    __table_args__ = {'comment': 'Пользователь'}
    user_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    first_name = Column(String(128), comment='Имя')
    last_name = Column(String(120), default='', comment='Фамилия')
    email = Column(String(128), comment='Электронная почта')

    def __repr__(self):
        return f"{self.user_id} {self.first_name} {self.last_name} {self.email}"