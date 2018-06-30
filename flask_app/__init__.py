from flask import Flask

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

from flask_restplus import Api
api = Api(app)


from flask_jwt_extended import JWTManager
jwt = JWTManager(app)

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
from flask_app.apiv1.__init__ import api1
app.register_blueprint(api1)

if __name__ == '__main__':
    app.run()
