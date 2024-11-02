from datetime import datetime
from instance.database import db

# User table with roles
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

class Professional(db.Model):
    __tablename__ = 'professionals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    service_type = db.Column(db.String(50))
    experience = db.Column(db.Integer)

    # Define the relationship with Service
    services = db.relationship('Service', back_populates='professional')

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    time_required = db.Column(db.String(50))
    approval_status = db.Column(db.String(20), default='Pending')
    total_orders = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)

    # Establish relationship with Professional
    professional = db.relationship('Professional', back_populates='services')
    
# Service Request table with relationships to User, Professional, and Service
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)  # Foreign key to Service
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Customer ID (User table)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)  # Assigned Professional

    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Requested')  # E.g., 'Requested', 'Assigned', 'Completed', 'Closed'
    rating = db.Column(db.Float, nullable=True)
    comments = db.Column(db.Text, nullable=True)
