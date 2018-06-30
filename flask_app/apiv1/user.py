from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_csrf_token, current_user
from flask_restplus import Api, Resource, Namespace

userapi = Namespace('users', description='Authorization API')

@userapi.route('/Foo')
class Users(Resource):
    @jwt_required
    def get(self):
        return {'message': 'Hi! {USER}. This is a GET response'.format(USER=current_user.username)}

    @jwt_required
    def post(self):
        return {'message': 'Hi! {USER}'.format(USER=current_user.username)}