# app/__init__.py
from dotenv import load_dotenv
from .routes import main
from flask import Flask

import lark_oapi as lark
import os
# 初始化项
load_dotenv()

def create_app():
    app = Flask(__name__)

    # 路由注册
    app.register_blueprint(main)
    return app