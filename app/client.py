# app/client.py

# 用于创建飞书的客户端并配置客户端参数

import lark_oapi as lark
from app.event_listening import handler

app_id = "cli_a67f3a534379500c"
app_shar = "67T6g2DuVq6ZZZj3uvTG7fHPaxxpKbwm"


def start_lark_client():
   cli = lark.ws.Client(
      lark.APP_ID,
      lark.APP_SECRET,
      event_handler=handler,
      log_level = lark.LogLevel.DEBUG
   )
   cli.start()