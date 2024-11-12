from flask_jwt_extended import jwt_required, get_jwt_identity
from instance.api import api
from flask_restful import Resource
from flask import request, jsonify
from instance.database import db
from application.models import User,Service,ServiceRequest, Professional
from datetime import timedelta,datetime
from sqlalchemy import func   

class UCartAPI(Resource):
    def get(self):
        # Fetch items with quantity > 0 in the cart
        cart_items = ServiceRequest.query.filter(ServiceRequest.quantity > 0).all()
        return jsonify([{
            "id": item.id,
            "service_id": item.service_id,
            "service": {
                "name": item.service.name,
                "base_price": item.service.base_price
            },
            "quantity": item.quantity
        } for item in cart_items])

class PlaceOrderAPI(Resource):
    def post(self):
        data = request.get_json()
        booking_date_str = data.get("booking_date")
        booking_time = data.get("booking_time")
        services = data.get("services")
        total_cost = data.get("total_cost")

        # Convert date and time
        booking_date = datetime.strptime(f"{booking_date_str} {booking_time}", "%Y-%m-%d %I:%M %p")

        # Create service requests for each service in the order
        for service_data in services:
            service_id = service_data.get("service_id")
            quantity = service_data.get("quantity")

            service_request = ServiceRequest(
                service_id=service_id,
                user_id=current_user.id,  # Assume you have current user ID available
                booking_date=booking_date,
                date_of_request=datetime.now(),
                status='Requested'
            )
            db.session.add(service_request)
        
        db.session.commit()
        return jsonify({"message": "Order placed successfully!"})

class ProfessionalDashboardAPI(Resource):
    def put(self, request_id):
        data = request.get_json()
        action = data.get("action")
        professional_id = current_user.id  # Assume you have professional's user ID available

        service_request = ServiceRequest.query.get(request_id)

        if not service_request:
            return jsonify({"message": "Service request not found"}), 404

        if action == "accept":
            service_request.professional_id = professional_id
            service_request.status = 'Assigned'
        elif action == "complete":
            service_request.status = 'Completed'

        db.session.commit()
        return jsonify({"message": "Service request updated successfully!"})

# Register API resources
api.add_resource(UCartAPI, '/api/ucart')
api.add_resource(PlaceOrderAPI, '/api/place_order')
api.add_resource(ProfessionalDashboardAPI, '/api/professional_dashboard/<int:request_id>')
