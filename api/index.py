from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
import jwt
from datetime import datetime, timedelta
import bcrypt

app = Flask(__name__)
CORS(app, 
     origins=["https://github-pratik.github.io"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS")
        return response, 200

# Rest of your code... 