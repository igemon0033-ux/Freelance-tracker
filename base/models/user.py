from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    categories = Column(String)
    exchanges = Column(String)
    kwork_budget = Column(Integer)
    notifications = Column(Integer)
    ads = Column(Integer)
    is_active = Column(Integer)
