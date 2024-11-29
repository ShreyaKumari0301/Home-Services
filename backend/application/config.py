import os 
from datetime import datetime, timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(".env")

if os.getenv("SECRET_KEY"):
    print("Environment Variables Fetched Successfully")
else:
    print("Something is wrong with Enviroment Variables.")


# configuration 
class Config():
    DEBUG = True  # Enable debugging
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')  # Database URI
    SECRET_KEY = os.getenv('SECRET_KEY')  # Secret key for authentication
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')  # JWT Secret Key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=2)  # Token expiration time
    SECURITY_TOKEN_AUTHENTICATION_HEADER = os.getenv('SECURITY_TOKEN_AUTHENTICATION_HEADER')  # Token header
    UPLOAD_FOLDER = 'uploads'  # Folder for file uploads
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt', 'docx'}  # Allowed file types
    MAX_CONTENT_LENGTH = 1024 * 1024  # Max upload size (1MB)

    # Mail configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'false').lower() in ['true', '1']  # Convert string to boolean
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # Celery configuration
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

    # Timezone settings
    ENABLE_UTC = os.getenv('ENABLE_UTC', 'false').lower() in ['true', '1']
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')

    # Cache configuration
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL")
    



    
    