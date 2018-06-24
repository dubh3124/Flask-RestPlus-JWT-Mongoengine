from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from flask_app.users.model import User
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt, set_access_cookies,set_refresh_cookies, unset_access_cookies, unset_refresh_cookies, unset_jwt_cookies, jwt_refresh_token_required)

auth = Blueprint('auth', __name__)

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)

user = User()
class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        try:
            user.username = data['username']
            user.password = user.generate_hash(data['password'])
            user.save()

            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])

            resp = jsonify({
                'message': 'User {} was created'.format(data['username'])
            })

            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)

            return resp
        except Exception as e:
            if "E11000 duplicate key error collection" in e.args[0]:
                return {'message': 'User {} already exists'.format(data['username'])}
            else:
                return {'message': 'Oops'}


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.objects(username__exact=data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}



        if user.verify_hash(data['password'], current_user.get().password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])

            resp = jsonify({
                'message': 'Logged in as {}'.format(current_user.get().username),
            })

            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp

        else:
            return {'message': 'Wrong credentials'}

class UserLogout(Resource):
    def post(self):
        try:
            resp = jsonify({'logout': True})
            unset_jwt_cookies(resp)
            return resp
        except:
            return jsonify({'error':'Something went wrong deleting token'})

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            resp = jsonify({'message':'Token Refreshed!'})
            set_access_cookies(resp, access_token)
            return resp
        except:
            return jsonify({'error':'Something went wrong refreshing token'})

api = Api(auth)
api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/token/refresh')
