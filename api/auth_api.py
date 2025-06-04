from flask import Blueprint, request, jsonify
from model import db, User, bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/users/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Username already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(
        username=data["username"], password=hashed_pw, email=data.get("email")
    )
    db.session.add(new_user)
    db.session.flush()  # Assigns ID before commit

    user_id = new_user.id  # Safe to access here

    db.session.commit()

    return jsonify({"message": "User registered", "user_id": user_id})


@auth_api.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(
            identity=user.id, expires_delta=timedelta(days=1)
        )
        return jsonify({"message": "Login successful", "token": access_token})

    return jsonify({"message": "Invalid credentials"}), 401
