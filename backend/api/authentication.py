from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from instance.api import api
from flask_restful import Resource
from flask import request, jsonify
from instance.database import db
from application.models import User,Service,ServiceRequest, Professional
from datetime import timedelta,datetime
from sqlalchemy import func

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
        print("processing the login request")
        data = request.get_json()
        print("data received")
        print(data)
        email= data.get('email')
        print(email)
        password = data.get('password')
        print(password)
        if not email or not password:
            return jsonify({'message': 'Invalid Inputs'}), 404
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        if not check_password_hash(user.password, password):
            return jsonify({'message': 'Incorrect Password'}), 401
        access_token = create_access_token(identity=email, expires_delta=timedelta(days=2))
        print("Ravi")
        return {'access_token': access_token, 'username' : user.name , 'userrole' : user.role},200
        # if data.get('email') and data.get('password'):
        #     email = data['email']
        #     password=data['password']
        #     user_from_db = User.query.filter_by(email=email).first()
        #     if user_from_db and check_password_hash(user_from_db.password, password):
        #         access_token = create_access_token(identity=email, expires_delta=timedelta(days=2))
        #         name = user_from_db.name
        #         role = user_from_db.role
        #         return {'access_token': access_token , 'username' : name , 'userrole' : role}, 200
        #     return {'message': 'Incorrect Credentials'} , 401
        # return {'message': 'Bad Request'} , 400
api.add_resource(TestAPI,'/test')
api.add_resource(RegistrationAPI, '/register')
api.add_resource(UserLoginAPI, '/login')