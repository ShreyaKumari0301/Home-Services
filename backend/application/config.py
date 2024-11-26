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
    DEBUG = True 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_TOKEN_AUTHENTICATION_HEADER = os.getenv('SECURITY_TOKEN_AUTHENTICATION_HEADER')
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt', 'docx'}
    MAX_CONTENT_LENGTH= 1024 * 1024
    



    
    