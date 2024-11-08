import os
from instance.app import app
from dotenv import load_dotenv
from utils.configuration import create_app , initialise_database 
from flask import Flask, request, jsonify
import api

import api
load_dotenv()
app = create_app()
initialise_database()






@app.route("/")
def home():
    return '<h1>Backend server Status : Running.</h1> <br> <a href="http://localhost:5173/">Click here to Access the frontend.</a>'


if __name__ == '__main__':
    # logger.info("Server Started")
    app.run(debug=True)
    
    