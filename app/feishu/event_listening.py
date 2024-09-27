# app/feishu/event_listening.py

# 处理事件监听相关的代码 主要用于接收飞书传递过来的事件流

# 事件处理函数
def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    print(lark.JSON.marshal(data))

# 创建事件分发处理器
event_handler = lark.EventDispatcherHandler.builder(
    ENCRYPT_KEY, VERIFICATION_TOKEN, lark.LogLevel.DEBUG
).register_p2_im_message_receive_v1(do_p2_im_message_receive_v1).build()
