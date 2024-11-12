
# professional



from flask_jwt_extended import jwt_required, get_jwt_identity
from instance.api import api
from flask_restful import Resource
from flask import request, jsonify
from instance.database import db
from application.models import User,Service,ServiceRequest, Professional
from datetime import timedelta,datetime
from sqlalchemy import func   
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



# api.add_resource(AddService,'/addservice')
# api.add_resource(DelService,'/delservice/<int:id>')
# api.add_resource(UpdService,'/updservice/<int:id>')
# api.add_resource(FetchService,'/fetchservice/<int:id>')





#api.add_resource(ProLoginAPI,'/')