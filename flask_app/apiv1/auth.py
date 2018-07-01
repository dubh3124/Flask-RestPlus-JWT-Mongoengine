from flask import jsonify
from flask_restplus import Resource, Namespace, fields
from flask_app.models.user import User
from flask_jwt_extended import (JWTManager,create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies, jwt_refresh_token_required)

jwt = JWTManager()

authapi = Namespace('auth', description='Authorization API')

creds = authapi.model('Credentials', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

user = User()


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    if not User.objects(username__exact=identity):
        return None

    return User.objects(username__exact=identity).get()


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return jsonify(ret), 404


@authapi.route('/registration')
# @api.doc(False)
class UserRegistration(Resource):
    @authapi.expect(creds)
    def post(self):
        data = authapi.payload

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


@authapi.route('/login')
class UserLogin(Resource):
    @authapi.expect(creds)
    def post(self):
        data = authapi.payload
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


@authapi.route('/logout')
class UserLogout(Resource):
    def post(self):
        try:
            resp = jsonify({'logout': True})
            unset_jwt_cookies(resp)
            return resp
        except:
            return jsonify({'error': 'Something went wrong deleting token'})


@authapi.route('/token/refresh')
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            resp = jsonify({'message': 'Token Refreshed!'})
            set_access_cookies(resp, access_token)
            return resp
        except:
            return jsonify({'error': 'Something went wrong refreshing token'})
