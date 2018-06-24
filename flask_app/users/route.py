from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, get_csrf_token
from flask_restful import Api, Resource

users = Blueprint('users', __name__)


class Users(Resource):
    def get(self):
        return {'user' : 'user'}

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        return {'message': 'User registration'}

api = Api(users)
api.add_resource(Users, '/Foo')
