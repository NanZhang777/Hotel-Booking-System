from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import Guest
from database import db

jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(guest):
    return guest.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Guest.query.get(identity)