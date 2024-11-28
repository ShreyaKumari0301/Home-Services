from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from instance.api import api
from flask_restful import Resource
from flask import request, jsonify
from instance.database import db
from application.models import User, Service, ServiceRequest, Professional, Customer
from datetime import timedelta, datetime
from sqlalchemy import func   
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ProfessionalSignup(Resource):
    def post(self):
        try:
            # Validate form fields
            required_fields = ['name', 'email', 'password', 'mobileNumber', 'pincode', 
                             'serviceCategory', 'experience', 'aadharCard']
            
            for field in required_fields:
                if field not in request.form:
                    return {"message": f"Missing required field: {field}"}, 400

            # Extract form data
            name = request.form['name']
            email = request.form['email'].lower()
            password = request.form['password']
            mobile_number = request.form['mobileNumber']
            pincodes = request.form['pincode'].split(',')  # Split comma-separated pincodes
            service_category = request.form['serviceCategory']
            experience = request.form['experience']
            aadhar_card = request.form['aadharCard']

            # Validate email uniqueness
            if Professional.query.filter_by(email=email).first():
                return {"message": "Email already registered"}, 400

            # Validate mobile number
            if len(mobile_number) != 10 or not mobile_number.isdigit():
                return {"message": "Mobile number must be exactly 10 digits"}, 400

            # Validate each pincode
            for pincode in pincodes:
                pincode = pincode.strip()  # Remove any whitespace
                if len(pincode) != 6 or not pincode.isdigit():
                    return {"message": f"Invalid pincode: {pincode}. Each pincode must be exactly 6 digits"}, 400

            # Handle document upload
            if 'document' not in request.files:
                return {"message": "Document is required"}, 400

            document = request.files['document']
            if not document or not allowed_file(document.filename):
                return {"message": "Invalid file type"}, 400

            if document.content_length > MAX_FILE_SIZE:
                return {"message": "File size exceeds 5MB limit"}, 400

            document_data = document.read()

            # Create professional instance
            professional = Professional(
                name=name,
                email=email,
                password=generate_password_hash(password),
                mobile_number=mobile_number,
                available_pincodes=','.join(pincodes),  # Store as comma-separated string
                service_category=service_category,
                experience=int(experience),
                aadhar_card=aadhar_card,
                ratings=0.0,
                document=document_data,
                role='Professional',
                status='pending'
            )

            db.session.add(professional)
            db.session.commit()
            
            return {"message": "Professional registration successful. Pending admin approval."}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": f"Registration failed: {str(e)}"}, 500

class ProfessionalServiceRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"message": "Professional not found"}, 404

            # Check if professional is blocked
            if professional.status.lower() == 'blocked':
                return {
                    "message": "Your account has been blocked. Contact administrator for assistance.",
                    "status": "blocked",
                    "confirmed_requests": ServiceRequest.query
                        .join(Service)
                        .join(Customer)
                        .filter(
                            ServiceRequest.professional_id == professional.id,
                            ServiceRequest.status == 'confirmed'
                        ).all()
                }, 403

            # Get available service requests only if professional is approved
            if professional.status.lower() != 'approved':
                return {"message": "Your account is pending approval"}, 403

            # Convert professional's pincodes string to list
            available_pincodes = professional.get_pincodes()

            # Get available service requests
            service_requests = ServiceRequest.query\
                .join(Service)\
                .join(Customer)\
                .filter(
                    ServiceRequest.professional_id.is_(None),
                    Service.category == professional.service_category,
                    ServiceRequest.status == 'pending',
                    ServiceRequest.service_pincode.in_(available_pincodes)
                ).all()

            results = [{
                "id": req.id,
                "service_name": req.service.name,
                "quantity": req.quantity,
                "total_price": float(req.total_price),
                "booking_date": req.booking_date.strftime("%Y-%m-%d"),
                "time_slot": req.time_slot,
                "customer_name": req.customer.name,
                "customer_phone": req.customer.mobile_number,
                "customer_address": req.customer.address,
                "service_pincode": req.service_pincode,
                "status": req.status
            } for req in service_requests]

            return jsonify(results)

        except Exception as e:
            return {"message": f"Error fetching requests: {str(e)}"}, 500

    @jwt_required
    def put(self):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"message": "Professional not found"}, 404

            data = request.get_json()
            request_id = data.get("service_request_id")
            
            if not request_id:
                return {"message": "service_request_id is required"}, 400

            service_request = ServiceRequest.query.get(request_id)
            
            if not service_request:
                return {"message": "Service request not found"}, 404

            if service_request.professional_id:
                return {"message": "Service request already assigned"}, 400

            service_request.professional_id = professional.id
            service_request.status = 'confirmed'  # Changed from 'assigned' to 'confirmed'
            service_request.assigned_at = datetime.utcnow()
            
            db.session.commit()
            return {"message": "Service request accepted successfully"}

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error accepting request: {str(e)}"}, 500


class ProfessionalProfile(Resource):
    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"message": "Professional not found"}, 404

            return {
                "name": professional.name,
                "email": professional.email,
                "mobile_number": professional.mobile_number,
                "service_category": professional.service_category,
                "experience": professional.experience,
                "ratings": float(professional.ratings),
                "status": professional.status,
                "available_pincodes": professional.available_pincodes
            }

        except Exception as e:
            return {"message": f"Error fetching profile: {str(e)}"}, 500

    @jwt_required()
    def put(self):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"message": "Professional not found"}, 404

            data = request.get_json()
            
            # Update allowed fields
            allowed_updates = ['name', 'mobile_number', 'available_pincodes']
            for field in allowed_updates:
                if field in data:
                    setattr(professional, field, data[field])

            db.session.commit()
            return {"message": "Profile updated successfully"}

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating profile: {str(e)}"}, 500

class ProfessionalActiveServices(Resource):
    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"message": "Professional not found"}, 404

            active_services = ServiceRequest.query\
                .join(Service)\
                .join(User)\
                .filter(
                    ServiceRequest.professional_id == professional.id,
                    ServiceRequest.status.in_(['assigned', 'in_progress'])
                ).all()

            results = [{
                "id": service.id,
                "service_name": service.service.name,
                "user_name": service.user.name,
                "booking_date": service.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
                "status": service.status,
                "total_price": float(service.total_price)
            } for service in active_services]

            return jsonify(results)

        except Exception as e:
            return {"message": f"Error fetching active services: {str(e)}"}, 500

    @jwt_required()
    def put(self):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"message": "Professional not found"}, 404

            data = request.get_json()
            service_id = data.get("service_id")
            new_status = data.get("status")

            if not service_id or not new_status:
                return {"message": "service_id and status are required"}, 400

            if new_status not in ['in_progress', 'completed']:
                return {"message": "Invalid status"}, 400

            service = ServiceRequest.query.get(service_id)
            
            if not service or service.professional_id != professional.id:
                return {"message": "Service request not found"}, 404

            service.status = new_status
            if new_status == 'completed':
                service.completed_at = datetime.utcnow()

            db.session.commit()
            return {"message": f"Service status updated to {new_status}"}

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating service status: {str(e)}"}, 500

class ProfessionalRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"error": "Professional not found"}, 404

            service_requests = ServiceRequest.query\
                .join(Service)\
                .join(Customer)\
                .filter(ServiceRequest.professional_id == professional.id)\
                .all()

            return jsonify([{
                'id': req.id,
                'service_name': req.service.name,
                'customer_name': req.customer.name,
                'customer_phone': req.customer.mobile_number,
                'booking_date': req.booking_date.strftime("%Y-%m-%d"),
                'time_slot': req.time_slot,
                'status': req.status,
                'rating': req.rating,
                'total_price': float(req.total_price)
            } for req in service_requests])

        except Exception as e:
            return {"error": str(e)}, 500

    @jwt_required()
    def put(self, request_id, action=None):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"error": "Professional not found"}, 404

            service_request = ServiceRequest.query.get(request_id)
            
            if not service_request or service_request.professional_id != professional.id:
                return {"error": "Service request not found"}, 404

            if action == 'accept':
                if service_request.status != 'pending':
                    return {"error": "Can only accept pending requests"}, 400
                service_request.status = 'confirmed'
            elif action == 'complete':
                if service_request.status != 'confirmed':
                    return {"error": "Can only complete confirmed requests"}, 400
                service_request.status = 'completed'
            
            db.session.commit()
            return {"message": f"Service request {action}ed successfully"}

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

class ProfessionalSummary(Resource):
    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"error": "Professional not found"}, 404

            # Get status distribution
            status_stats = db.session.query(
                ServiceRequest.status,
                func.count(ServiceRequest.id)
            ).filter(ServiceRequest.professional_id == professional.id)\
            .group_by(ServiceRequest.status)\
            .all()

            # Get monthly earnings
            monthly_earnings = db.session.query(
                func.strftime('%Y-%m', ServiceRequest.booking_date).label('month'),
                func.sum(ServiceRequest.total_price)
            ).filter(
                ServiceRequest.professional_id == professional.id,
                ServiceRequest.status == 'completed'
            ).group_by('month').all()

            # Get rating distribution
            rating_distribution = db.session.query(
                ServiceRequest.rating,
                func.count(ServiceRequest.id)
            ).filter(
                ServiceRequest.professional_id == professional.id,
                ServiceRequest.rating.isnot(None)
            ).group_by(ServiceRequest.rating).all()

            # Get pincode stats
            pincode_stats = db.session.query(
                ServiceRequest.service_pincode,
                func.count(ServiceRequest.id)
            ).filter(
                ServiceRequest.professional_id == professional.id,
                ServiceRequest.status == 'completed'
            ).group_by(ServiceRequest.service_pincode).all()

            return {
                'status_stats': dict(status_stats),
                'monthly_earnings': dict(monthly_earnings),
                'rating_distribution': dict(rating_distribution),
                'pincode_stats': dict(pincode_stats)
            }

        except Exception as e:
            return {"error": str(e)}, 500

class ProfessionalStats(Resource):
    @jwt_required()
    def get(self):
        try:
            email = get_jwt_identity()
            professional = Professional.query.filter_by(email=email).first()
            
            if not professional:
                return {"error": "Professional not found"}, 404

            # Calculate total earnings
            total_earnings = db.session.query(
                func.sum(ServiceRequest.total_price)
            ).filter(
                ServiceRequest.professional_id == professional.id,
                ServiceRequest.status == 'completed'
            ).scalar() or 0

            # Overall rating is already stored in professional.ratings
            overall_rating = professional.ratings or 0

            return {
                "overall_rating": float(overall_rating),
                "total_earnings": float(total_earnings)
            }

        except Exception as e:
            return {"error": str(e)}, 500

# Register API resources
api.add_resource(ProfessionalSignup, '/professional/signup')
api.add_resource(ProfessionalServiceRequests, '/professional/service-requests')
api.add_resource(ProfessionalProfile, '/professional/profile')
api.add_resource(ProfessionalActiveServices, '/professional/active-services')
api.add_resource(ProfessionalRequests, 
    '/professional/requests',
    '/professional/requests/<int:request_id>/<string:action>'
)
api.add_resource(ProfessionalSummary, '/professional/summary')
api.add_resource(ProfessionalStats, '/professional/stats')