# app/routes.py

# 路由管理
from flask import Blueprint
from app.event_listening import handler
from lark_oapi.adapter.flask import *
from lark_oapi.api.im.v1 import *
from app.client import start_lark_client




main = Blueprint('main', __name__)

@main.route('/')
def home():
   return "Hello World"

@main.route("/event")
def start():
   return start_lark_client()



