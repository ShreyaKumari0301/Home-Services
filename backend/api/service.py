from flask_jwt_extended import jwt_required, get_jwt_identity
from instance.api import api
from flask_restful import Resource
from flask import request, jsonify
from instance.database import db
from application.models import User,Service,ServiceRequest, Professional
from datetime import timedelta,datetime
from sqlalchemy import func   

class ServiceRequestAPI(Resource):
    def get(self):
        requests = ServiceRequest.query.all()
        data = [{
            'id': request.id,
            'service': {
                'name': request.service.name,
                'category': request.service.category,
                'price': request.service.base_price,
                'time_required': request.service.time_required,
            },
            'quantity': 1,  
            'booking_date': request.booking_date,
            'status': request.status,
            'professional': {
                'name': request.professional.name,
                'rating': request.professional.rating,
                'phone': request.professional.phone,
            },
        } for request in requests]
        return jsonify(data)

    def put(self, request_id):
        data = request.get_json()
        service_request = ServiceRequest.query.get_or_404(request_id)

        if 'new_booking_date' in data:
            new_booking_date = datetime.strptime(data['new_booking_date'], '%Y-%m-%d %I:%M %p')
            service_request.booking_date = new_booking_date
            service_request.status = 'Rescheduled'

        db.session.commit()
        return {'message': 'Service request updated successfully'}, 200

    def post(self):
        data = request.get_json()
        try:
            booking_date_str = data.get('booking_date')
            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d %H:%M')  # Format: 'YYYY-MM-DD HH:MM'
            
            if booking_date > datetime.now() + timedelta(days=2):
                return {'message': 'Booking can only be made up to 2 days in advance.'}, 400

            new_request = ServiceRequest(
                service_id=data['service_id'],
                user_id=data['user_id'],
                professional_id=data['professional_id'],
                date_of_request=datetime.now(),
                status="Requested",
                booking_date=booking_date,
                rating=data.get('rating', None),
                comments=data.get('comments', "")
            )
            db.session.add(new_request)
            db.session.commit()

            return {'message': 'Service request created successfully'}, 201
        except ValueError as ve:
            return {'message': f'Invalid date format: {ve}'}, 400
        except Exception as e:
            return {'message': str(e)}, 500
    
    def delete(self, request_id):
        service_request = ServiceRequest.query.get(request_id)
        
        if not service_request:
            return {'message': 'Service request not found'}, 404

        db.session.delete(service_request)
        db.session.commit()
        return {'message': 'Service request deleted successfully'}, 200

    @staticmethod
    def format_service_request(service_request):
        return {
            'id': service_request.id,
            'service_id': service_request.service_id,
            'user_id': service_request.user_id,
            'professional_id': service_request.professional_id,
            'date_of_request': service_request.date_of_request.strftime('%Y-%m-%d %H:%M:%S'),
            'status': service_request.status,
            'rating': service_request.rating,
            'comments': service_request.comments,
            'booking_date': service_request.booking_date.strftime('%Y-%m-%d %H:%M')
        }

class ProfileAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'name': user.name,
                'email': user.email,
                'mobile_number': user.mobile_number,
                'address': user.address
            })
        return {'message': 'User not found'}, 404

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        user = User.query.get(user_id)
        if user:
            user.name = data.get('name', user.name)
            user.mobile_number = data.get('mobile_number', user.mobile_number)
            user.address = data.get('address', user.address)
            db.session.commit()
            return {'message': 'Profile updated successfully'}
        return {'message': 'User not found'}, 404
            

class ServiceList(Resource):
    def get(self):
        """Fetch all services, optionally filtered by category."""
        category = request.args.get('category')
        services = Service.query.filter_by(category=category) if category else Service.query.all()
        return jsonify([service.to_dict() for service in services])

    def post(self):
        """Add a new service."""
        data = request.json
        new_service = Service(name=data['name'], base_price=data['base_price'], category=data['category'])
        db.session.add(new_service)
        db.session.commit()
        return jsonify(new_service.to_dict()), 201


class ServiceAction(Resource):
    def put(self, service_id):
        """Edit a service."""
        data = request.json
        service = Service.query.get(service_id)
        if not service:
            return {'message': 'Service not found'}, 404
        service.name = data['name']
        service.base_price = data['base_price']
        service.category = data['category']
        db.session.commit()
        return jsonify(service.to_dict())

    def delete(self, service_id):
        """Delete a service."""
        service = Service.query.get(service_id)
        if not service:
            return {'message': 'Service not found'}, 404
        db.session.delete(service)
        db.session.commit()
        return {'message': 'Service deleted'}, 200


class ProfessionalList(Resource):
    def get(self):
        """Fetch all professionals."""
        professionals = Professional.query.all()
        return jsonify([prof.to_dict() for prof in professionals])

    def post(self):
        """Add a new professional."""
        data = request.json
        new_professional = Professional(
            name=data['name'], experience=data['experience'], category=data['category'], document=data['document']
        )
        db.session.add(new_professional)
        db.session.commit()
        return jsonify(new_professional.to_dict()), 201


class ProfessionalAction(Resource):
    def put(self, professional_id):
        """Approve, reject, block, or remove a professional."""
        data = request.json
        professional = Professional.query.get(professional_id)
        if not professional:
            return {'message': 'Professional not found'}, 404
        action = data.get('action')
        if action == 'approve':
            professional.status = 'approved'
        elif action == 'reject':
            professional.status = 'rejected'
        elif action == 'block':
            professional.status = 'blocked'
        elif action == 'remove':
            db.session.delete(professional)
        db.session.commit()
        return jsonify(professional.to_dict())


class ServiceRequestList(Resource):
    def get(self):
        # Fetch all services, optionally filtering by category or search term
        category = request.args.get('category')
        search_query = request.args.get('search_query', '').lower()

        query = Service.query

        # Filter by category if provided
        if category:
            query = query.filter_by(category=category)

        # Filter by search query if provided
        if search_query:
            query = query.filter(Service.name.ilike(f"%{search_query}%"))

        services = query.all()
        return jsonify([service.to_dict() for service in services])

    def post(self):
        # Add a new service
        data = request.get_json()
        new_service = Service(
            name=data['name'],
            base_price=data['base_price'],
            category=data['category']
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify(new_service.to_dict()), 201

class CategoryList(Resource):
    def get(self):
        # Retrieve distinct categories from services
        categories = db.session.query(Service.category).distinct().all()
        category_list = [category[0] for category in categories]
        return jsonify(category_list)

# professional
class ProfessionalHomeResource(Resource):
    def get(self, professional_id):
        # Fetch service requests assigned to the professional with 'Requested' status
        requests = ServiceRequest.query.filter_by(
            professional_id=professional_id,
            status="Requested"
        ).all()
        result = [{
            "id": req.id,
            "customer_name": User.query.get(req.user_id).name,
            "booking_date": req.booking_date,
            "contact_phone": User.query.get(req.user_id).phone,
            "location": req.location,
            "pincode": req.pincode
        } for req in requests]
        return jsonify(result)

    def put(self, request_id):
        # Accept or reject a service request
        req = ServiceRequest.query.get_or_404(request_id)
        action = request.json.get('action')  # "accept" or "reject"
        
        if action == "accept":
            req.status = "Assigned"
        elif action == "reject":
            req.status = "Rejected"
        else:
            return {"message": "Invalid action"}, 400
        
        db.session.commit()
        return {"message": f"Service request {action}ed successfully"}, 200

class CompletedServicesResource(Resource):
    def get(self, professional_id):
        # Fetch completed services, with optional filtering
        search_date = request.args.get('date')
        location = request.args.get('location', '').lower()
        pincode = request.args.get('pincode', '')

        query = ServiceRequest.query.filter_by(
            professional_id=professional_id,
            status="Completed"
        )

        # Apply filters if provided
        if search_date:
            query = query.filter(func.date(ServiceRequest.booking_date) == search_date)
        if location:
            query = query.filter(ServiceRequest.location.ilike(f"%{location}%"))
        if pincode:
            query = query.filter(ServiceRequest.pincode == pincode)

        completed_requests = query.all()
        result = [{
            "id": req.id,
            "customer_name": User.query.get(req.user_id).name,
            "booking_date": req.booking_date,
            "rating": req.rating,
            "review": req.review,
            "location": req.location,
            "pincode": req.pincode
        } for req in completed_requests]
        return jsonify(result)

class ProfessionalSummaryResource(Resource):
    def get(self, professional_id):
        # Service request status summary
        status_summary = db.session.query(
            ServiceRequest.status, func.count(ServiceRequest.id)
        ).filter_by(professional_id=professional_id).group_by(ServiceRequest.status).all()
        
        # Rating summary
        rating_summary = db.session.query(
            ServiceRequest.rating, func.count(ServiceRequest.id)
        ).filter_by(professional_id=professional_id).group_by(ServiceRequest.rating).all()

        status_data = {status: count for status, count in status_summary}
        rating_data = {rating: count for rating, count in rating_summary}

        return jsonify({
            "service_request_status": status_data,
            "ratings": rating_data
        })

# API Routes
api.add_resource(ProfessionalHomeResource, '/professional/<int:professional_id>/home', '/api/service_request/<int:request_id>/action')
api.add_resource(CompletedServicesResource, '/professional/<int:professional_id>/completed_services')
api.add_resource(ProfessionalSummaryResource, '/professional/<int:professional_id>/summary')


# Add resources to API
api.add_resource(ServiceList, '/services')
api.add_resource(ServiceAction, '/services/<int:service_id>')
api.add_resource(ProfessionalList, '/professionals')
api.add_resource(ProfessionalAction, '/professionals/<int:professional_id>')
api.add_resource(ServiceRequestList, '/service-requests')
api.add_resource(CategoryList, '/categories')



# api.add_resource(AddService,'/addservice')
# api.add_resource(DelService,'/delservice/<int:id>')
# api.add_resource(UpdService,'/updservice/<int:id>')
# api.add_resource(FetchService,'/fetchservice/<int:id>')
api.add_resource(ServiceRequestAPI, '/service_requests', '/service_requests/<int:request_id>')
api.add_resource(ProfileAPI, '/profile')





#api.add_resource(ProLoginAPI,'/')