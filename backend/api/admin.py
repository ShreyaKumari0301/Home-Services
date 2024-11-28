from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from instance.api import api
from flask_restful import Resource
from flask import request, jsonify, send_file
from instance.database import db
from application.models import User,Service,Professional,Customer,ServiceRequest
from datetime import timedelta
from flask_jwt_extended import jwt_required
from utils.role_required import role_required   
from flask_jwt_extended import get_jwt_identity
import io
from flask import current_app as app
from sqlalchemy.sql import func


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
    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            user = User.query.filter_by(email=email).first()
            if not user or user.role != 'Admin':
                return {'message': 'Unauthorized access'}, 401

            professionals = Professional.query.all()
            return jsonify([{
                'id': p.id,
                'name': p.name,
                'email': p.email,
                'mobile_number': p.mobile_number,
                'service_category': p.service_category,
                'experience': p.experience,
                'ratings': p.ratings,
                'status': p.status
            } for p in professionals])
        except Exception as e:
            return {'message': str(e)}, 500

    @jwt_required()
    def put(self, professional_id):
        try:
            email = get_jwt_identity()
            user = User.query.filter_by(email=email).first()
            if not user or user.role != 'Admin':
                return {'message': 'Unauthorized access'}, 401

            data = request.get_json()
            professional = Professional.query.get(professional_id)
            
            if not professional:
                return {'message': 'Professional not found'}, 404

            current_status = professional.status.lower()
            new_status = data['status'].lower()
            
            valid_transitions = {
                'pending': ['approved', 'rejected'],
                'approved': ['blocked'],
                'blocked': ['approved'],
                'rejected': ['approved']
            }

            if new_status not in valid_transitions.get(current_status, []):
                return {
                    'message': f'Invalid status transition from {current_status} to {new_status}'
                }, 400
                
            professional.status = new_status
            db.session.commit()
            
            return {'message': 'Status updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500
        
class CustomerManagement(Resource):
    @jwt_required()
    def get(self):
        try:
            # Get the current user's email from JWT
            email = get_jwt_identity()
            
            # Verify if the user is admin
            user = User.query.filter_by(email=email).first()
            if not user or user.role != 'Admin':
                return {'message': 'Unauthorized access'}, 401

            customers = Customer.query.all()
            return jsonify([{
                'id': c.id,
                'name': c.name,
                'email': c.email,
                'mobile_number': c.mobile_number,
                'address': c.address,
                'pincode': c.pincode,
                'status': c.status
            } for c in customers])
        except Exception as e:
            return {'message': str(e)}, 500

    @jwt_required()
    def put(self, customer_id):
        try:
            # Get the current user's email from JWT
            email = get_jwt_identity()
            
            # Verify if the user is admin
            user = User.query.filter_by(email=email).first()
            if not user or user.role != 'Admin':
                return {'message': 'Unauthorized access'}, 401

            data = request.get_json()
            customer = Customer.query.get(customer_id)
            
            if not customer:
                return {'message': 'Customer not found'}, 404
                
            customer.status = data['status']
            db.session.commit()
            
            return {'message': 'Status updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

# Add this to your existing api.add_resource calls
api.add_resource(CustomerManagement, 
    '/admin/customers', 
    '/admin/customers/<int:customer_id>/status'
)

api.add_resource(AdminAPI,'/adminservice','/adminservice/<int:id>')
api.add_resource(ProfessionalManagement, 
    '/admin/professionals', 
    '/admin/professionals/<int:professional_id>/status'
)

class ProfessionalDocument(Resource):
    @jwt_required()
    def get(self, professional_id):
        try:
            professional = Professional.query.get(professional_id)
            if not professional:
                return {"error": "Professional not found"}, 404
                
            return send_file(
                io.BytesIO(professional.document),
                mimetype='application/octet-stream',
                as_attachment=True,
                download_name=f'document_{professional_id}.pdf'
            )
        except Exception as e:
            return {"error": str(e)}, 500

# Update the API resource registration
api.add_resource(ProfessionalDocument, '/admin/professionals/<int:professional_id>/document')

class SummaryAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            # First verify if user is admin
            email = get_jwt_identity()
            user = User.query.filter_by(email=email).first()
            if not user or user.role != 'Admin':
                return {'message': 'Unauthorized access'}, 401

            # Get category distribution
            category_distribution = db.session.query(
                Service.category, 
                func.count(ServiceRequest.id)
            ).join(ServiceRequest).group_by(Service.category).all()
            
            # Get professional status distribution
            prof_status = db.session.query(
                Professional.status, 
                func.count(Professional.id)
            ).group_by(Professional.status).all()
            
            # Get top 3 professionals by rating
            top_professionals = db.session.query(
                Professional.name, 
                Professional.ratings
            ).order_by(Professional.ratings.desc()).limit(3).all()
            
            # Get rating distribution
            rating_dist = db.session.query(
                ServiceRequest.rating,
                func.count(ServiceRequest.id)
            ).filter(ServiceRequest.rating.isnot(None)
            ).group_by(ServiceRequest.rating).all()
            
            return {
                'category_distribution': dict(category_distribution),
                'professional_status': dict(prof_status),
                'top_professionals': [
                    {'name': name, 'rating': rating} 
                    for name, rating in top_professionals
                ],
                'rating_distribution': dict(rating_dist)
            }
            
        except Exception as e:
            return {'message': str(e)}, 500

api.add_resource(SummaryAPI, '/admin/summary')

class ServiceRequestManagement(Resource):
    @jwt_required()
    def get(self, view_type=None):
        try:
            email = get_jwt_identity()
            user = User.query.filter_by(email=email).first()
            if not user or user.role != 'Admin':
                return {'message': 'Unauthorized access'}, 401

            if view_type == 'completed':
                # For ARequests - only completed services with ratings
                requests = ServiceRequest.query\
                    .join(Service)\
                    .join(Customer)\
                    .filter(ServiceRequest.status == 'completed')\
                    .order_by(ServiceRequest.rating.desc())\
                    .all()
            else:
                # For AHome - pending and confirmed services
                requests = ServiceRequest.query\
                    .join(Service)\
                    .join(Customer)\
                    .filter(ServiceRequest.status.in_(['pending', 'confirmed']))\
                    .order_by(ServiceRequest.booking_date.desc())\
                    .all()

            return jsonify([{
                'id': req.id,
                'service_name': req.service.name,
                'customer_name': req.customer.name,
                'customer_email': req.customer.email,
                'customer_phone': req.customer.mobile_number,
                'booking_date': req.booking_date.strftime("%Y-%m-%d"),
                'time_slot': req.time_slot,
                'status': req.status,
                'rating': req.rating,
                'total_price': float(req.total_price),
                'service_details': {
                    'category': req.service.category,
                    'description': req.service.description,
                    'time_required': req.service.time_required
                }
            } for req in requests])

        except Exception as e:
            return {'message': str(e)}, 500

    @jwt_required()
    def put(self, request_id):
        try:
            email = get_jwt_identity()
            user = User.query.filter_by(email=email).first()
            if not user or user.role != 'Admin':
                return {'message': 'Unauthorized access'}, 401

            data = request.get_json()
            service_request = ServiceRequest.query.get(request_id)
            
            if not service_request:
                return {'message': 'Service request not found'}, 404

            if data.get('action') == 'accept':
                service_request.status = 'confirmed'
            elif data.get('action') == 'reject':
                service_request.status = 'cancelled'
            
            db.session.commit()
            return {'message': f'Service request {data["action"]}ed successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

# Update API resources
api.add_resource(ServiceRequestManagement, 
    '/admin/requests',
    '/admin/requests/completed',
    '/admin/requests/<int:request_id>'
)


            