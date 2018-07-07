
from flask_app.db_init import FlaskDocument
from flask_app.models.user import User

def register(app):
    @app.cli.command()
    def resetdb():
        ResetDB().run()

    @app.cli.command()
    def populatedb():
        PopulateDB().run()

class ResetDB:
    """Drops all tables and recreates them"""
    def run(self):
        self.drop_collections()

    def drop_collections(self):
        for klass in FlaskDocument.all_subclasses():
            klass.drop_collection()


class PopulateDB():
    """Fills in predefined data to DB"""
    def run(self):
        self.create_users()

    @staticmethod
    def create_users():
        users = []
        for u in (('matt', 'matt@lp.com', 'password', ['admin'], True, 'Matt', 'Jenkins'),
                  ('joe', 'joe@lp.com', 'password', ['editor'], True, 'Joe', 'Jackson'),
                  ('jill', 'jill@lp.com', 'password', ['author'], True, 'Jill', 'Jane'),
                  ('tiya', 'tiya@lp.com', 'password', [], False, 'Tiya', 'Willams'),
                  ('dubh3124', 'dubh3124@lp.com', 'password', [], True, 'Herman', 'Haggerty')):
            user = User(
                username=u[0],
                email=u[1],
                password=User().generate_hash(u[2]),
                active=u[4],
                firstname=u[5],
                lastname=u[6]
            )
            users.append(user)

        User.objects.insert(users)




