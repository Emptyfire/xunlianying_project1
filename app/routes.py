# app/routes.py

# 路由管理
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/event", methods=["POST"])
def event():
    resp = event_handler.do(parse_req())
    return parse_resp(resp)

