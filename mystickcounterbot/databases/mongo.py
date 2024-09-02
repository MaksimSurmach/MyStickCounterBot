from datetime import datetime

import certifi
from pymongo.mongo_client import MongoClient

from mystickcounterbot.models.data import UserMetaData, StickActivityMetadata


class MongoDB:
    def __init__(self, uri: str, db_name: str, username: str, password: str):
        self.db = None
        self.name = db_name
        self.uri = uri
        self.username = username
        self.password = password
        self.client = MongoClient(f"mongodb+srv://{username}:{password}@{uri}/{db_name}?retryWrites=true&w=majority",
                                  tlsCAFile=certifi.where(), tlsAllowInvalidCertificates=True)

    def connect(self):
        try:
            self.client.server_info()
            self.client.admin.command('ping')
            return True
        except ConnectionError as e:
            print(e)
            return False

    def close(self):
        self.client.close()

    def init_db(self):
        """
        Get the collection from the database
        :return:
        """
        self.db = self.client[self.name]
        collections = self.db.list_collection_names()
        # check if the collection exists
        if "users" not in collections:
            self.db.create_collection("users")
        if "stick_activity" not in collections:
            self.db.create_collection("stick_activity")
        return

    def insert(self, collection: str, data: dict):
        try:
            self.db[collection].insert_one(data)
            return True
        except Exception as e:
            print(e)
            return False

    def find(self, collection: str, query: dict):
        try:
            return self.db[collection].find(query)
        except Exception as e:
            print(e)
            return None

    def update(self, collection: str, query: dict, data: dict):
        try:
            self.db[collection].update_one(query, {"$set": data})
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self, collection: str, query: dict):
        try:
            self.db[collection].delete_one(query)
            return True
        except Exception as e:
            print(e)
            return False

    def add_stick(self, data: dict):
        try:
            self.db.stick_activity.insert_one(data)
            return True
        except Exception as e:
            print(e)
            return False

    def remove_last_cigarette(self, user_id: int, count: int = 1):
        if count < 0:
            return False
        if count == 0:
            return True
        else:
            last = self.db.stick_activity.find(
                {"user_id": user_id},
                sort=[("timestamp", -1)],
                limit=count
            )
            if last:
                for item in last:
                    self.db.stick_activity.delete_one({"_id": item.get("_id")})
                return True
            return False

    def get_total_cigarettes_today(self, user_id: int):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.db.stick_activity.count_documents(
            {"user_id": user_id, "timestamp": {"$gte": today}}
        )

    def get_last_cigarette_time(self, user_id: int):
        last = self.db.stick_activity.find_one(
            {"user_id": user_id},
            sort=[("timestamp", -1)]
        )
        if last:
            return last.get("timestamp")

    def create_user(self, data: dict):
        try:
            self.db.users.insert_one(data)
            return True
        except Exception as e:
            print(e)
            return False

    def get_user(self, user_id: int):
        raw_data = self.db.users.find_one({"user_id": user_id})
        user = UserMetaData(user_id=0)
        for key in UserMetaData.__fields__.keys():
            if key in raw_data:
                setattr(user, key, raw_data[key])

        return user if user.user_id != 0 else None

    def set_user_goal(self, user_id: int, goal: int):
        try:
            self.db.users.update_one({"user_id": user_id}, {"$set": {"goals.daily_goal": goal}})
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_goal(self, user_id: int):
        user = self.db.users.find_one({"user_id": user_id})
        if user is None:
            return None
        return user.get("goals", {}).get("daily_goal", 0)
