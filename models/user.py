from typing import Dict, Union
from mongoengine import Document, StringField, BooleanField

from mongo_config import db


UserJSON = Dict[str, Union[int, str]]


class UserModel(Document):
    """

    Attributes:
        useremail (str): The useremail of the user.
        password (str): The password of the user.
        username (str): The username of the user.
        adresse (str): The address of the user.
    """

    users = db["users"]
    useremail = StringField(required=True, max_length=1)
    password = StringField(required=True)
    username = StringField(required=True)
    adresse = StringField(required=True)
    activated = BooleanField(default=False)

    # verify correct password
    @classmethod
    def find_by_useremail(cls, useremail: str) -> "UserModel":

        return cls.users.find({useremail: useremail})

    @classmethod
    def verify_pw(cls, useremail: str, password: str) -> bool:
        if cls.users.find({"useremail": useremail}).count() == 0:
            return False
        else:
            pass_wd = cls.users.find({"useremail": useremail})[0]["password"]
            if pass_wd == password:
                return True
            else:
                return False

    @classmethod
    def user_exist(cls, useremail: str) -> bool:
        """
        Retrieves a user from the MongoDB database with the given username.
        representing the retrieved user, or None if the user was not found.

        Args:
            username (str): The username of the user to retrieve.
        """
        if cls.users.find({"useremail": useremail}).count() == 0:
            return False
        else:
            return True
