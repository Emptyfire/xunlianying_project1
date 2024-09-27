# app/event_listening.py
import lark_oapi as lark
# 处理事件监听相关的代码 主要用于接收飞书传递过来的消息事件流

def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    print(lark.JSON.marshal(data))


def do_customized_event(data: lark.im.v1.P2ImMessageMessageReadV1) -> None:
    print(lark.JSON.marshal(data))

# 飞书事件处理器
handler = lark.EventDispatcherHandler.builder(lark.ENCRYPT_KEY,
                                               lark.VERIFICATION_TOKEN,
                                                 lark.LogLevel.DEBUG) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .register_p2_drive_file_bitable_record_changed_v1(do_customized_event)\
    .build()