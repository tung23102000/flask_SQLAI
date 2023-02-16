from multiprocessing import connection
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity,jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel
import sqlite3
#private attr
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='This field cannot be blank.')
_user_parser.add_argument('password', type=str, required=True, help='This field cannot be blank.')

class UserRegister(Resource):
   
    def post(self):
        data =  _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": 'A user with this username already exists'},400
        # c1: user = UserModel(data['username'],data['password'])
        user = UserModel(**data)
        user.save_to_db()
            
            
        return {"message": "User created successfully"},201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"},404
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"},404
        user.delete_from_db()
        return {'message': "User deleted"},200
    
    
class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data= _user_parser.parse_args()
        # find user in database
        user = UserModel.find_by_username(data['username'])
        # check password, # create access token ,# create refresh token
        # => this is what the `identity()` userd to do
        if user and user.password==data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            },200
        return {'message': 'Invalid credentials'},401
    
    
class TokenRefresh(Resource):
    # We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
    @jwt_required(refresh=True)
    def post(self):
          current_user = get_jwt_identity()
          # If we are refreshing a token here we have not verified the users password in
# a while, so mark the newly created access token as not fresh
          new_token = create_access_token(identity=current_user, fresh=False)
          return {'access_token': new_token},200
