from flask_jwt_extended import jwt_required, get_jwt_identity
from instance.api import api
from flask_restful import Resource
from flask import request, jsonify
from instance.database import db
from application.models import User,Service,ServiceRequest, Professional, Customer
from datetime import timedelta,datetime
from utils.role_required import role_required
#from sqlalchemy import func   
#from utils.role_required import role_required
#from utils.tasks import send_mail_task
#from instances.caches import cache

# class CategoryList(Resource):
#     def get(self):
#         # Retrieve distinct categories from services
#         categories = db.session.query(Service.category).distinct().all()
#         category_list = [category[0] for category in categories]
#         return jsonify(category_list)


class ServiceListResource(Resource):
    def get(self, service_id=None):
        # If service_id is provided, fetch a single service
        if service_id:
            service = Service.query.filter_by(id=service_id).first()
            if not service:
                return {"error": "Service not found"}, 404
            
            return {
                "id": service.id,
                "name": service.name,
                "base_price": service.base_price,
                "description": service.description,
                "category": service.category,
                "time_required": service.time_required,
                "avg_rating": service.avg_rating,
            }, 200
        
        # If service_id is not provided, fetch all services with optional filters
        search = request.args.get("search", "")
        category = request.args.get("category", "")

        query = Service.query
        if category:
            query = query.filter(Service.category.ilike(f"%{category}%"))
        if search:
            query = query.filter(Service.name.ilike(f"%{search}%"))

        services = query.all()
        return [
            {
                "id": s.id,
                "name": s.name,
                "base_price": s.base_price,
                "description": s.description,
                "category": s.category,
                "time_required": s.time_required,
                "avg_rating": s.avg_rating,
            }
            for s in services
        ], 200

class CreateServiceRequest(Resource):
    def post(self):
        data = request.json
        required_fields = [
            'service_id', 'email', 'booking_date',
            'time_slot', 'quantity', 'total_price'
        ]
        
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing {field}"}, 400

        try:
            email = data['email']
            customer = Customer.query.filter_by(email=email).first()
            
            if not customer:
                return {"error": "Customer not found"}, 404

            # Find professionals who can service this pincode
            matching_professionals = Professional.query\
                .join(Service, Service.category == Professional.service_category)\
                .filter(
                    Service.id == data['service_id'],
                    Professional.status == 'approved',
                    Professional.available_pincodes.like(f"%{customer.pincode}%")
                ).all()

            if not matching_professionals:
                return {"error": "No service providers available in your area"}, 400

            # Create the service request
            new_request = ServiceRequest(
                service_id=data['service_id'],
                customer_id=customer.id,
                booking_date=datetime.strptime(data['booking_date'], '%Y-%m-%d'),
                time_slot=data['time_slot'],
                quantity=data['quantity'],
                total_price=data['total_price'],
                service_pincode=customer.pincode,
                status='pending'
            )

            db.session.add(new_request)
            db.session.commit()

            return {
                "message": "Service request created successfully",
                "request_id": new_request.id
            }, 201
        
        except ValueError as e:
            return {"error": f"Invalid date format: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

class CustomerDetails(Resource):
    def get(self):
        email = request.args.get('email')
        
        if not email:
            return {"error": "Email is required"}, 400
        
        try:
            customer = Customer.query.filter_by(email=email).first()
            
            if not customer:
                return {"error": "Customer not found"}, 404
            
            return {
                "id": customer.id,
                "pincode": customer.pincode,
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 500

class CustomerServiceRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            customer = Customer.query.filter_by(email=email).first()
            
            if not customer:
                return {"error": "Customer not found"}, 404

            service_requests = ServiceRequest.query\
                .join(Service)\
                .outerjoin(Professional)\
                .filter(ServiceRequest.customer_id == customer.id)\
                .all()

            results = [{
                "id": req.id,
                "service_name": req.service.name,
                "booking_date": req.booking_date.strftime("%Y-%m-%d"),
                "time_slot": req.time_slot,
                "quantity": req.quantity,
                "total_price": float(req.total_price),
                "status": req.status,
                "professional_details": {
                    "name": req.professional.name,
                    "phone": req.professional.mobile_number,
                    "rating": float(req.professional.ratings)
                } if req.professional else None
            } for req in service_requests]

            return jsonify(results)

        except Exception as e:
            return {"error": str(e)}, 500

# Add resource to API
api.add_resource(CustomerDetails, '/customer-details')


# api.add_resource(CategoryList, '/categories')
api.add_resource(ServiceListResource,'/services', '/services/<int:service_id>')
api.add_resource(CreateServiceRequest, '/service-requests')
api.add_resource(CustomerServiceRequests, '/customer/service-requests')
