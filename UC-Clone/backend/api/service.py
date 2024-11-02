from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from instance.api import api
from flask_restful import Resource
from flask import request
from instance.database import db
from application.models import User , Service
from datetime import timedelta

class ServiceAPI(Resource):
    def get(self):
        services = Service.query.all()
        return 