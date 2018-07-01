from flask_app import create_app, script

app = create_app()
script.register(app)