from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import json,requests
from utils.connect import client, db, fs

auth = Blueprint("auth", __name__)
authEmails = ['elvis8333', 'mahendrasir', 'amurto8317', 'bhate8318', 'carol8320', 'mahesh8328', 'sherwin8358', 'cassia8374']
@auth.route("/signup", methods=["POST"])
def register():
    user = json.loads(request.data)
    print(user)
    flag = False
    first_name = user.get("first_name")
    last_name = user.get("last_name")
    email = user.get("email")
    if email.split('@')[0] not in authEmails:
        return jsonify({"success": False, "message": "User Not authorized."}), 409
    password = user.get("password")
    if first_name == None or last_name == None or email == None or password == None:
        return jsonify({"success": False, "message": "Fields are empty."}), 401
    test = db.users.find_one({"email": email})

    if test:
        return jsonify({"success": False, "message": "User Already Exist."}), 409
    else:
        user_info = dict(first_name=first_name, last_name=last_name, email=email, password=password)
        inserted = db.users.insert_one(user_info)
        access_token = create_access_token(identity=email) #token
        return jsonify({"success": True, "message": "User added sucessfully.", "userId": str(inserted.inserted_id), "token": access_token}), 201


@auth.route("/signin", methods=["POST"])
def login():
    user = json.loads(request.data)
    email = user.get("email")
    password = user.get("password")
    if email == None or password == None:
        return jsonify({"success": False, "message": "Fields are empty."}), 401
    test = db.users.find_one({"email": email, "password": password})
    if test:
        access_token = create_access_token(identity=email) #token
        return jsonify({"success": True, "message": "Login Succeeded!", "userId": str(test["_id"]), "token": access_token}), 201
    else:
        return jsonify({"success": False, "message": "Bad Email or Password"}), 401