import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False

    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

    VNP_TMN_CODE = os.getenv("VNP_TMN_CODE")
    VNP_SECRET_KEY = os.getenv("VNP_SECRET_KEY")
    VNP_URL = os.getenv("VNP_URL", "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html")
    VNP_RETURN_URL = os.getenv("VNP_RETURN_URL", "http://127.0.0.1:5000/transaction/payment_return")

    BASE_URL = "http://127.0.0.1:5000"

    URL_SELENIUM= os.getenv('URL_SELENIUM')

    PAGE_SIZE = 6