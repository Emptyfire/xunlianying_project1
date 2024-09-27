# app/client.py

# 用于创建飞书的客户端并配置客户端参数

import lark_oapi as lark
from app.event_listening import bitable_event_handler


def start_lark_client():
    cli = lark.ws.Client('cli_a67f3a534379500c', '67T6g2DuVq6ZZZj3uvTG7fHPaxxpKbwm',
                         event_handler=bitable_event_handler,
                         log_level=lark.LogLevel.DEBUG)
    cli.start()