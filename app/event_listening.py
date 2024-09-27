# app/event_listening.py
import lark_oapi as lark
# 处理事件监听相关的代码 主要用于接收飞书传递过来的事件流

#定义事件处理函数
def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    print(f'[ do_p2_im_message_receive_v1 access ], data: {lark.JSON.marshal(data, indent=4)}')

#构建事件处理器
bitable_event_handler = lark.EventDispatcherHandler.builder("", "") \
    .register_p2_drive_file_bitable_record_changed_v1(do_p2_im_message_receive_v1) \
    .build()