from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from instance.api import api

from flask_restful import Resource
from flask import request
from instance.database import db
from application.models import User, Customer, Professional
from datetime import timedelta

# from utils.tasks import send_mail_task


class RegistrationAPI(Resource):
    def post(self):
        data = request.get_json()
        print("processing the request")
        if data.get('name') and data.get('email') and data.get('password'):
            if User.query.filter_by(email=data['email']).first():
                return {'message': 'User already exists'}, 409
            else:
                user = Customer(
                    name = data['name'],
                    email = data['email'].lower(),
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
        if not (data.get('email') and data.get('password')):
            return {'message': 'Missing email or password'}, 400

        user_from_db = User.query.filter_by(email=data['email']).first()
        
        if not user_from_db:
            return {'message': 'User not found'}, 401

        if user_from_db.role == 'User':
            customer = Customer.query.get(user_from_db.id)
            if customer and customer.status == 'Blocked':
                return {'message': 'Your account has been blocked. Please contact administrator.'}, 403
        elif user_from_db.role == 'Professional':
            professional = Professional.query.get(user_from_db.id)
            print(professional)
            if professional:
                if professional.status == 'Blocked':
                    print("hello")
                    return {'message': 'Your account has been blocked. Please contact administrator.'}, 403
                elif professional.status == 'Pending':
                    return {'message': 'Your account is currently under review. Please wait for admin approval.'}, 403

        if check_password_hash(user_from_db.password, data['password']):
            access_token = create_access_token(identity=data['email'], expires_delta=timedelta(days=2))
            return {
                'access_token': access_token,
                'username': user_from_db.name,
                'userrole': user_from_db.role
            }, 200

        return {'message': 'Incorrect credentials'}, 401


# Add resources to API
api.add_resource(RegistrationAPI, '/register')
api.add_resource(UserLoginAPI, '/login')




















# from source import generate_password_hash, check_password_hash
# from flask_jwt_extended import create_access_token
# from instance.api import api
# from flask_restful import Resource
# from flask import request, jsonify
# from instance.database import db
# from application.models import User,Service
# from datetime import timedelta
# # from utils.tasks import send_mail_task



# class RegistrationAPI(Resource):
#     def post(self):
#         data = request.get_json()
#         print("processing the request")
#         if data.get('name') and data.get('email') and data.get('password'):
#             if User.query.filter_by(email=data['email']).first():
#                 return {'message': 'User already exists'}, 409
#             else:   
#                 user = User(
#                     name = data['name'],
#                     email = data['email'],
#                     password=generate_password_hash(data['password']),
#                     mobile_number=data.get('mobile_number', ''),
#                     address=data.get('address',''),
#                     pincode=data.get('pincode',''),
#                     role="User"
#                 )
#                 db.session.add(user)
#                 db.session.commit()
#                 print("sending the response")
#                 return {'message': 'User Registration Successful. You can login now.'} ,201
            
    
# class UserLoginAPI(Resource):
#     def post(self):
#         data = request.get_json()
#         if data.get('email') and data.get('password'):
#             email = data['email']
#             password=data['password']
#             user_from_db = User.query.filter_by(email=email).first()
#             if user_from_db and check_password_hash(user_from_db.password, password):
#                 access_token = create_access_token(identity=email, expires_delta=timedelta(days=2))
#                 name = user_from_db.name
#                 role = user_from_db.role
#                 return {'access_token': access_token , 'username' : name , 'userrole' : role}, 200
#             return {'message': 'Incorrect Credentials'} , 401
#         return {'message': 'Bad Request'} , 400


# api.add_resource(RegistrationAPI, '/register')
# api.add_resource(UserLoginAPI, '/login')



# #api.add_resource(ProRegistrationAPI,'/')
# #api.add_resource(ProLoginAPI,'/')