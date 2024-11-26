from instance.app import app
from instance.database import db
from instance.api import api
from application.config import Config
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager

from flask_cors import CORS
from application.models import User



def create_app():
    app.config.from_object(Config)
    db.init_app(app)
    api.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    return app



def initialise_database():
    with app.app_context():
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()

        if not table_names:  # If no tables exist
            db.create_all()
            print("Database created successfully.")

            # Admin Account
            admin_email = input("Enter Admin Email Address: ")
            admin_password = input("Create an Admin password: ")
            hashed_password = generate_password_hash(admin_password)
            # admin_mob = input("Enter Admin mobile number: ")
            # admin_add = input("Enter Admin address: ")
            # admin_pin = input("Enter Admin pin code: ")


            admin_profile = User(
                name='Admin',
                email=admin_email,
                password=hashed_password,
                role="Admin",
                mobile_number="None",
                # address="None",
                # pincode="None"
            )
        
            
            # Adding roles and admin user to the database
            try:
                db.session.add(admin_profile)
                db.session.commit()
                print("Admin profile created successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating database roles or admin profile: {e}")
        else:
            print("Database already exists.")
