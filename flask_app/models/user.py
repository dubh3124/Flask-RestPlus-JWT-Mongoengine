import datetime
from flask_app.db_init import db, FlaskDocument
from passlib.hash import pbkdf2_sha256 as sha256


class User(FlaskDocument):
    email = db.StringField(max_length=255)
    username = db.StringField(max_length=255, unique=True)
    firstname = db.StringField(max_length=255)
    lastname = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)