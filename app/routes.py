# app/routes.py

# 路由管理
from flask import Blueprint


main = Blueprint('main', __name__)

@main.route('/')
def home():
   return "Hello World"

