from feishu.means import uget_tenant_access_token
from feishu.means import uget_record
import lark_oapi as lark
from _thread import _excepthook, _ExceptHookArgs, get_native_id as get_native_id
import threading, asyncio

excepthook = _excepthook
ExceptHookArgs = _ExceptHookArgs

def do_record_change(data: lark.drive.v1.P2DriveFileBitableRecordChangedV1) -> None:
    global last_data
    last_data = data

    lark.logger.info(f"[do_record_change access] handle incoming event, event_id: {data.header.event_id}, table_id: {data.event.table_id}, revision: {data.event.revision}")
    lark.logger.debug(f"[do_record_change access] data:{lark.JSON.marshal(data, indent=4)}")

event_handler = lark.EventDispatcherHandler.builder("", "") \
        .register_p2_drive_file_bitable_record_changed_v1(do_record_change) \
        .build()

ws_client = lark.ws.Client(
      "cli_a67f3a534379500c", \
      "67T6g2DuVq6ZZZj3uvTG7fHPaxxpKbwm",\
      event_handler = event_handler,\
      log_level = lark.LogLevel.INFO)

client = lark.Client.builder() \
        .app_id("cli_a67f3a534379500c") \
        .app_secret("67T6g2DuVq6ZZZj3uvTG7fHPaxxpKbwm") \
        .log_level(lark.LogLevel.INFO) \
        .build()


ws_thread = threading.Thread(target = ws_client.start)
threading.excepthook = excepthook
ws_thread.start()


print(uget_tenant_access_token())

#print(uget_record())