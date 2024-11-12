from datetime import datetime
from instance.database import db

# User table with roles
#from sqlalchemy import CheckConstraint

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    mobile_number = db.Column(db.String(10), nullable=False)

    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())
    pincode = db.Column(db.String(100), nullable=False)  # Comma-separated list, up to 10 pincodes
    #__table_args__ = (CheckConstraint("length(split_part(pincodes, ',', 10)) <= 10", name="max_10_pincodes"),)

class User(Person):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    role = db.Column(db.String(20), default='user')
    address = db.Column(db.String(255), nullable=False)  # Comma-separated list for multiple addresses

class Professional(Person):
    __tablename__ = 'professionals'
    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    service_category = db.Column(db.String(50), nullable=False)
    ratings = db.Column(db.Float, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    aadhar_card = db.Column(db.String(12), unique=True, nullable=False)  # Assuming 12-digit Aadhar card
    document = db.Column(db.LargeBinary, nullable=False)  # Add file size validation in form handling

'''class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    #address = db.Column(db.String(100),nullable = False)
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
'''
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50))
    time_required = db.Column(db.String(50))
    # approval_status = db.Column(db.String(20), default='Pending')
    #total_orders = db.Column(db.Integer, default=0)
    avg_rating = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "base_price": self.base_price,
            "category": self.category
        }

    # Establish relationship with Professional
    #professional = db.relationship('Professional', back_populates='services')
    
# Service Request table with relationships to User, Professional, and Service
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)  # Foreign key to Service
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Customer ID (User table)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)  # Assigned Professional
    date_of_request = db.Column(db.DateTime,nullable = False)
    booking_date = db.Column(db.DateTime, nullable=False)  
    status = db.Column(db.String(20), default='Requested')  # E.g., 'Requested', 'Assigned', 'Completed', 'Closed'
    rating = db.Column(db.Float, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    # user = db.Relationship('User', foreign_keys=[user_id])
    # professional = db.Relationship('User', foreign_keys=[professional_id])
    # service = db.Relationship('Service', foreign_keys=[service_id])
    service = db.relationship('Service', backref='service_requests')
    user = db.relationship('User', foreign_keys=[user_id], backref='service_requests')
    professional = db.relationship('User', foreign_keys=[professional_id], backref='professional_requests',
                                   primaryjoin="and_(ServiceRequest.professional_id == User.id, User.role == 'Professional')") 
    # professional = db.relationship('User', foreign_keys=[professional_id], backref='professional_requests')
    # user = db.relationship('User', backref='service_requests')
    # professional = db.relationship('Professional', backref='service_requests') 