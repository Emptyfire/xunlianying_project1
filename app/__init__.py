# app/__init__.py

from .routes import main
from flask import Flask
import os

ENCRYPT_KEY = os.getenv('ENCRYPT_KEY')
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# 初始化项
def create_app():
    app = Flask(__name__)

    # 路由注册
    app.register_blueprint(main)
    return app

