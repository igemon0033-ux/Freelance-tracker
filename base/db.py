from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from base.models.user import UserModel, Base
import json

oldBase = declarative_base()


class OldUserModel(oldBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    categories = Column(String)
    exchanges = Column(String)
    notifications = Column(Integer)


class Database:

    def __init__(self):
        self.engine = create_engine("sqlite:///users.db")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    # Add new user function
    def add_user(self, user_id: int):
        self.session = self.Session()
        self.user = self.session.query(UserModel).filter_by(id=user_id).first()
        if not self.user:
            self.new_user = UserModel(id=user_id, categories=json.dumps([]), notifications=1,
                                      exchanges=json.dumps(["kwork"]), ads=1, is_active=1, kwork_budget=0)
            self.session.add(self.new_user)
            self.session.commit()
            self.session.close()
        else:
            self.user.is_active = 1
            self.session.commit()
            self.session.close()
            return Exception("User is already added")

    # Change user category function
    def change_user_categories(self, user_id: int, new_categories):
        self.session = self.Session()
        self.user = self.session.query(UserModel).filter_by(id=user_id).first()
        if self.user:
            self.user.categories = json.dumps(new_categories, ensure_ascii=False)
            self.session.commit()
            self.session.close()
        else:
            self.session.close()
            return Exception("User not found")

    def change_user_kwork_budget(self, user_id: int, new_budget: int):
        self.session = self.Session()
        self.user = self.session.query(UserModel).filter_by(id=user_id).first()
        if self.user:
            self.user.kwork_budget = new_budget
            self.session.commit()
            self.session.close()
        else:
            self.session.close()
            return Exception("User not found")

    def change_user_exchanges(self, user_id: int, new_exchanges: json):
        self.session = self.Session()
        self.user = self.session.query(UserModel).filter_by(id=user_id).first()
        if self.user:
            self.user.exchanges = new_exchanges
            self.session.commit()
            self.session.close()
        else:
            self.session.close()
            return Exception("User not found")

    def get_user_exchanges(self, user_id: int):
        self.session = self.Session()
        self.user = self.session.query(UserModel).filter_by(id=user_id).first()
        self.session.close()
        if self.user:
            return eval(self.user.exchanges)
        else:
            return Exception("User not found")

    def get_user_categories(self, user_id: int):
        session = self.Session()
        user = session.query(UserModel).filter_by(id=user_id).first()
        session.close()
        if user:
            res = json.loads(user.categories)
            return res
        else:
            return Exception("User not found")

    def get_user_kwork_budget(self, user_id: int):
        session = self.Session()
        user = session.query(UserModel).filter_by(id=user_id).first()
        session.close()
        if user:
            return user.kwork_budget
        else:
            return 0

    def get_users_by_order(self, category: str, exchange: str):
        self.session = self.Session()
        self.userstrings = self.session.query(UserModel).filter(
            UserModel.categories.contains(category),
            UserModel.exchanges.contains(exchange),
            UserModel.notifications == 1
        ).all()
        self.session.close()
        users_ids = []
        for elem in self.userstrings:
            users_ids.append(elem.id)
        return users_ids

    def get_user_notifications(self, user_id: int):
        self.session = self.Session()
        self.user = self.session.query(UserModel).filter_by(id=user_id).first()
        self.session.close()
        if self.user:
            return self.user.notifications
        else:
            return Exception("User not found")

    def change_user_notification(self, user_id: int):
        self.session = self.Session()
        self.user = self.session.query(UserModel).filter_by(id=user_id).first()
        if self.user.notifications == 1:
            self.user.notifications = 0
        else:
            self.user.notifications = 1
        self.session.commit()
        self.session.close()

    def get_users_stats(self):
        session = self.Session()

        users = session.query(UserModel).count()
        real = session.query(UserModel).filter(UserModel.exchanges != "[]",
                                                       UserModel.categories != "[]",
                                                       UserModel.is_active).count()
        active_users = session.query(UserModel).filter(UserModel.exchanges != "[]",
                                                       UserModel.categories != "[]").count()

        return {"users": users, "active_users": active_users, "real_users": real}

    def get_user_ads(self, user_id: int):
        session = self.Session()
        user = session.query(UserModel).filter_by(id=user_id).first()
        session.close()
        if user:
            return user.ads
        else:
            return Exception("User not found")

    def hide_ads_for_user(self, user_id: int):
        session = self.Session()
        user = session.query(UserModel).filter_by(id=user_id).first()
        if user:
            user.ads = 0
        session.commit()
        session.close()

    def get_user_active(self, user_id: int):
        session = self.Session()
        user = session.query(UserModel).filter_by(id=user_id).first()
        session.close()
        if user:
            return user.is_active
        else:
            return Exception("User not found")

    def change_user_active(self, user_id: int):
        session = self.Session()
        user = session.query(UserModel).filter_by(id=user_id).first()
        if user:
            if user.is_active == 1:
                user.is_active = 0
            else:
                user.is_active = 1
            session.commit()
        else:
            return Exception("User not found")
        session.close()

    def get_all_users(self):
        session = self.Session()
        user_strings = session.query(UserModel).all()
        session.close()
        users_ids = []
        for elem in user_strings:
            users_ids.append(elem.id)
        return users_ids
