import logging
from flask import json
from .db_init import FlaskDocument
from .models.user import User
from .apiv1 import api


def register(app):
    @app.cli.command()
    def resetdb():
        ResetDB().run()

    @app.cli.command()
    def populatedb():
        PopulateDB().run()

    @app.cli.command()
    def getPostmanCollection():
        Postman().run()


class ResetDB:
    """Drops all tables and recreates them"""

    def run(self):
        self.drop_collections()

    def drop_collections(self):
        for klass in FlaskDocument.all_subclasses():
            klass.drop_collection()


class PopulateDB:
    """Fills in predefined data to DB"""

    def run(self):
        try:
            self.create_users()
        except Exception:
            logging.exception("Database contains data, resetting")
            ResetDB().drop_collections()

    @staticmethod
    def create_users():
        users = []
        for u in (
            ("matt", "matt@lp.com", "password", ["admin"], True, "Matt", "Jenkins"),
            ("joe", "joe@lp.com", "password", ["editor"], True, "Joe", "Jackson"),
            ("joey", "joey@lp.com", "password", ["editor"], True, "Joey", "Jackson"),
            ("jill", "jill@lp.com", "password", ["author"], True, "Jill", "Jane"),
            ("tiya", "tiya@lp.com", "password", [], False, "Tiya", "Willams"),
        ):
            user = User(
                username=u[0],
                email=u[1],
                password=User().generate_hash(u[2]),
                active=u[4],
                firstname=u[5],
                lastname=u[6],
            )
            users.append(user)

        User.objects.insert(users)


class Postman:
    def run(self):
        self.getPostmanCollection()

    def getPostmanCollection(self):
        data = api.as_postman(urlvars=False, swagger=True)
        print(json.dumps(data))
