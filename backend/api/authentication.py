from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from instance.api import api
from flask_restful import Resource
from flask import request, jsonify
from instance.database import db
from application.models import User
from datetime import timedelta

class TestAPI(Resource):
    def get(self):
        return {'message': 'API Working'}, 200

class RegistrationAPI(Resource):
    def post(self):
        data = request.get_json()
        print("processing the request")
        if data.get('name') and data.get('email') and data.get('password'):
            if User.query.filter_by(email=data['email']).first():
                return {'message': 'User already exists'}, 409
            else:
                user = User(
                    name = data['name'],
                    email = data['email'],
                    password=generate_password_hash(data['password']),
                    mobile_number=data.get('mobile_number', ''),
                    address=data.get('address',''),
                    pincode=data.get('pincode',''),
                    role="User"
                )
                db.session.add(user)
                db.session.commit()
                print("sending the response")
                return {'message': 'User Registration Successful. You can login now.'} ,201
            
    
class UserLoginAPI(Resource):
    def post(self):
        data = request.get_json()
        email= data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'message': 'Invalid Inputs'}), 404
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        if not check_password_hash(user.password, password):
            return jsonify({'message': 'Incorrect Password'}), 401
        access_token = create_access_token(identity=email, expires_delta=timedelta(days=2))
        return {'access_token': access_token, 'username' : user.name , 'userrole' : user.role},200
     
api.add_resource(TestAPI,'/test')
api.add_resource(RegistrationAPI, '/register')
api.add_resource(UserLoginAPI, '/login')