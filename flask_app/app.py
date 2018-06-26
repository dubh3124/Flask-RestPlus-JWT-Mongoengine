from flask import Flask
from flask_restful import Api

app = Flask(__name__)

app.config.from_object('flask_app.config.app_config')
app.logger.info("Config: %s" % app.config['ENVIRONMENT'])

#  Logging
import logging
logging.basicConfig(
    level=app.config['LOG_LEVEL'],
    format='%(asctime)s %(levelname)s: %(message)s '
           '[in %(pathname)s:%(lineno)d]',
    datefmt='%Y%m%d-%H:%M%p',
)

from flask_jwt_extended import JWTManager
JWTManager(app)

# CORS
from flask_cors import CORS
CORS(app, supports_credentials=True)

# Email
from flask_mail import Mail
app.mail = Mail(app)

# MongoEngine
from flask_app.db_init import db
app.db = db
app.db.init_app(app)

# Business Logic
# http://flask.pocoo.org/docs/patterns/packages/
# http://flask.pocoo.org/docs/blueprints/
from flask_app.users.route import users
from flask_app.auth.route import auth

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run()
