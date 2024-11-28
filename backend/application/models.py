from datetime import datetime
from instance.database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    mobile_number = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(20), default='user')
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())


class Customer(User):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(100), nullable=False) 
    status = db.Column(db.String(20), default='Accepted')   


class Professional(User):
    __tablename__ = 'professionals'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    service_category = db.Column(db.String(50), nullable=False)
    ratings = db.Column(db.Float, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending') #Pending, Approved, Rejected, blocked
    aadhar_card = db.Column(db.String(12), unique=True, nullable=False)
    document = db.Column(db.LargeBinary, nullable=False)  # document field can hold file data
    available_pincodes = db.Column(db.String(100), nullable=False) 
    def get_pincodes(self):
        """Convert stored pincode string to list"""
        return self.available_pincodes.split(',') if self.available_pincodes else []
    def set_pincodes(self, pincodes):
        """Convert list of pincodes to comma-separated string"""
        if isinstance(pincodes, list):
            self.available_pincodes = ','.join(map(str, pincodes))
        else:
            self.available_pincodes = str(pincodes)
            
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50))
    time_required = db.Column(db.String(50))
    avg_rating = db.Column(db.Float, default=0.0)

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "base_price": self.base_price,
    #         "category": self.category
    #     }

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), default=None)
    booking_date = db.Column(db.DateTime, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Requested') #requested, accpted, completed, cancelled
    rating = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    service_pincode = db.Column(db.String(100), nullable=False)
    service = db.relationship('Service', backref='service_requests')
    customer = db.relationship('Customer', backref='service_requests')
    professional = db.relationship('Professional', backref='service_requests')
    # cancelled_at = db.Column(db.DateTime, nullable=True)
