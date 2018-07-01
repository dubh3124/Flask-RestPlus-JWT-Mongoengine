from flask import Flask

def create_app():
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

    from flask_app.apiv1.auth import jwt
    jwt.init_app(app)

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
    from flask_app.apiv1 import api1
    app.register_blueprint(api1)

    # from flask_app.script import resetdb, populatedb
    # # Click Commands
    # app.cli
    # app.cli.add_command(resetdb)
    # app.cli.add_command(populatedb)

    return app