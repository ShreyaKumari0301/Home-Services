from instance.app import app
from instance.database import db
from instance.api import api
from application.config import Config
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager

from flask_cors import CORS
from application.models import User

from instance.mail import mail
from instance.caches import cache
from instance.celery import celeryservice

def create_app():
    app.config.from_object(Config)
    celeryservice.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celeryservice.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celeryservice.conf.enable_utc = app.config["ENABLE_UTC"]
    celeryservice.conf.timezone = app.config["TIMEZONE"]
    class ContextTask(celeryservice.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celeryservice.Task = ContextTask

    db.init_app(app)
    api.init_app(app)
    CORS(app)
    JWTManager(app)
    mail.init_app(app)
    cache.init_app(app)

    app.app_context().push()
    
    print("returning celery service")
    return celeryservice
    



def initialise_database():
    with app.app_context():
        from instance.caches import cache
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
