import os
from datetime import timedelta

class Config:
    # fixed secret key instead of random secret key
    SECRET_KEY = 'hotel-booking-platform-secret-key-2024-fixed'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hotel.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret-key-for-hotel-booking-2024-fixed'  # fixed value
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)  # set expiration