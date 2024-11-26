from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from instance.api import api
from flask_restful import Resource
from flask import request, jsonify
from instance.database import db
from application.models import User,Service,Professional
from datetime import timedelta
from flask_jwt_extended import jwt_required
from utils.role_required import role_required   


class AdminAPI(Resource):
    # @jwt_required
    # @role_required('admin')
    def post(self):
        data = request.get_json()
        required_fields = ['name', 'base_price', 'description', 'category', 'time_required']
        if not all(field in data and data[field] for field in required_fields):
            return {"message": "All fields are required."}, 400
        try:
            new_service = Service(
            name=data.get('name'),
            base_price=data.get('base_price'),
            description=data.get('description'),
            category=data.get('category'),
            time_required=data.get('time_required'),
            avg_rating=data.get('avg_rating', 0)
        )
            db.session.add(new_service)
            db.session.commit()
            return {"message": "Service created"}, 201
        except Exception as e:
            return {"message": "Error"}, 500
    
    # @jwt_required
    # @role_required('admin') 
    def put(self):
        data = request.get_json()
        id = data.get('id')
        service = Service.query.get(id)
        if not service:
            return {"message": "Service not found"}, 404
        service.name = data.get('name', service.name)
        service.base_price = data.get('base_price', service.base_price)
        service.description = data.get('description', service.description)
        service.category = data.get('category', service.category)
        service.time_required = data.get('time_required', service.time_required)
        service.avg_rating = data.get('avg_rating', service.avg_rating)
        db.session.commit()
        return {"message": "Service updated"}, 200       

    # @jwt_required
    # @role_required('admin')  
    def get(self):
        category = request.args.get('category')
        query = Service.query
        if category:
            query = query.filter_by(category=category)
        services = query.all()
        services_list = [
            {
                'id': service.id,
                'name': service.name,
                'base_price': service.base_price,
                'description': service.description,
                'category': service.category,
                'time_required': service.time_required,
                'avg_rating': service.avg_rating
            }
            for service in services
        ]
        return jsonify(services_list)
  


    # @jwt_required
    # @role_required('Admin') 
    def delete(self,id):
        service = Service.query.get(id)
        if service:
            db.session.delete(service)
            db.session.commit()
            return ({"message": "Service deleted"}), 200
        return {"message":"Service not found"},404
    
   
    

class ProfessionalManagement(Resource):
    # @jwt_required()
    # @role_required('admin')
    def get(self):
        try:
            professionals = Professional.query.all()
            return jsonify([{
                'id': p.id,
                'name': p.name,
                'email': p.email,
                'mobile_number': p.mobile_number,
                'service_category': p.service_category,
                'experience': p.experience,
                'status': p.status
            } for p in professionals])
        except Exception as e:
            return {'message': str(e)}, 500

    # @jwt_required()
    # @role_required('admin')
    def put(self, professional_id):
        try:
            data = request.get_json()
            professional = Professional.query.get(professional_id)
            
            if not professional:
                return {'message': 'Professional not found'}, 404
                
            professional.status = data['status']
            db.session.commit()
            
            return {'message': 'Status updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

api.add_resource(AdminAPI,'/adminservice','/adminservice/<int:id>')
api.add_resource(ProfessionalManagement, 
    '/admin/professionals', 
    '/admin/professionals/<int:professional_id>/status'
)


            