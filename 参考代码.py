import sys, io, atexit
import threading, asyncio
import code
import re
import lark_oapi as lark
import urllib.parse as parse
from datetime import datetime
from lark_oapi.api.auth.v3 import *
from lark_oapi.api.wiki.v2 import *
from lark_oapi.api.drive.v1 import *
from lark_oapi.api.bitable.v1 import *
from lark_oapi.api.im.v1 import *

# overall config
save_pics = False
pic_dir = "img/"
loglevel = lark.LogLevel.INFO
dedup_list_size = 20

# test app
#app_id = "cli_a67f3f4ae63d500e"
#app_secret = "dlldGo5ZoyiaLMwyKI8UTf3UbBBjYELV"
#file_token = "ZQ6NbSpZNaBzUrsEi2OcDmPbncf"
#table_id = "tbli5Rd4enup25ms"

# production app
app_id = "cli_a67b17d72e7a900b"
app_secret = "4XVYaGd04umVor0oSjrkicEeeKKqH125"
wiki_token = "SDlJwP51EiQH1ikJGJKcEazhnic" #测试大表 -> 健康生活营数据库
file_token = "" # 留空，由wiki_token自动获取file_token
#wiki_token = "" # 留空
#file_token = "JrHvbIpc4avMA6sdSp0ckH71nse" #植此青绿健康生活营数据记录表
table_name = "2024年9月-11月饮食记录表"
table1_name = "2024年9月-11月运动记录表"
#receive_id = "ou_ebad3939fb34bcf4ef8d482685004a12" # 孙天宇
#receive_id_type = "open_id"
#receive_id = "oc_151d83a170d782a087e6f3b33634cc01" # 测试群
#receive_id_type = "chat_id"
#receive_name = "植此青绿健康生活打卡群"
receive_name = "健康生活营饮食运动记录群"
receive_id = "" # 留空，由receive_name自动获取群聊id
receive_id_type = "chat_id"

# message templates
message_template = """
-------人员信息-------
🏋️{角色}： {创建人}
📌组别： {分组}
🕛餐次： {餐次}
-----食物计算&估算----
🍚主食种类： {🍚本餐主食①种类}
⚖️主食重量： {🍚本餐主食①重量（g）}g
🍗瘦肉①种类： {🍗本餐瘦肉①种类}
⚖️瘦肉①重量： {🍗本餐瘦肉①重量（g）}g
🥩瘦肉②种类： {🥛本餐瘦肉②种类}
⚖️瘦肉②重量： {🥛本餐瘦肉②重量（g）}g
---------碳水----------
✅本餐应吃碳水： {本餐应吃碳水}g
🗝️本餐碳水： {本餐碳水（g）}g
🔓已吃碳水： {已吃碳水量（g）}g
🔒今日剩余碳水配额: {今日剩余碳水配额}g
-------蛋白质--------
✅本餐应吃蛋白质： {本餐应吃蛋白质}g
🗝️本餐蛋白质： {本餐蛋白质（g）}g
🔓已吃蛋白质： {已吃蛋白质（g）}g
🔒今日剩余蛋白质配额： {今日剩余蛋白质配额}g
--------脂肪--------
✅本餐应吃脂肪： {本餐应吃脂肪}g
-------备注&补充-----
⏰填表时间： {登记日期}
🤔本餐感受： {本餐感受}
✍自评： {自评}
📌备注： {备注}
💥饱腹感： {本餐饱腹感}
-------------锐评召唤-----------
{教练员} {监督员}
"""

message1_template="""
🏃 {角色}： {创建人}
📌组别： {组别}
📆运动日期： {日期}
🏸运动项目： {运动项目}
👊运动强度： {运动强度}
✍️运动感受： {运动感受}
💥召唤： {教练员} {监督员}
"""

# global variables
#file_token = ""
table_id = ""
table1_id = ""
record_id = "recupDDWlVBxRb" # 测试记录
last_data = None
fields_list = None
fields_by_name = None
fields_by_id = None
fields1_list = None
fields1_by_name = None
fields1_by_id = None

marshal = lark.JSON.marshal
unmarshal = lark.JSON.unmarshal
dedup_list = [""]*dedup_list_size
dedup_list_ptr = 0

subscription_table = {}

# debug
debug_item = None
task_list = set()

def field_value_to_string(value, field_type=None, field_property=None) -> str:
    if type(value) == int:
        if field_type == 5: #date
            date = datetime.fromtimestamp(value/1000)
            if field_property.date_formatter == "yyyy/MM/dd":
                return date.strftime("%Y/%m/%d")
            elif field_property.date_formatter == "yyyy/MM/dd HH:mm":
                return date.strftime("%Y/%m/%d %H:%m")
            else:
                return date.strftime("%Y/%m/%d %H:%m")
        else:
            return str(value)
    if type(value) == float:
        return str(value)
    if type(value) == str:
        return value
    if type(value) == dict:
        if value["type"] == 3:
            return value["value"][0]
        if value["type"] == 2:
            return str(value["value"][0])
        if value["type"] == 1:
            value = value["value"]
            return value[0]["text"]
        if value["type"] == 11: # personnel record
            #assume only 1 item
            #lark.logger.debug(f"formatting value: {value}")
            value = value["value"][0]
            return f"<at user_id=\"{value['id']}\">{value['name']}</at>"
    if type(value) == list:
        if field_type == 17: # picture
            string = ""
            for pic in value:
                string += f"[picture {pic['name']}]"
            return string
        if field_type == 1: # text
            return value[0]["text"]
        if field_type == 11 or field_type == 1003: # personnel record
            #assume only 1 item
            #lark.logger.debug(f"formatting value: {value}")
            value = value[0]
            return f"<at user_id=\"{value['id']}\">{value['name']}</at>"
    else:
        lark.logger.error(f"unrecognized value: {value}")
        return ""

def split_message(message: str) -> list:
    result = []
    p = 0
    at_iter = re.finditer('<at user_id="([^"]*)">([^<>]*)</at>', message)
    for match in at_iter:
        result.append({"tag": "text", "text": message[p:match.start()]})
        result.append({"tag": "at", "user_id": match.group(1)})
        p = match.end()
    result.append({"tag": "text", "text": message[p:]})
    return result
            
async def retrieve_pictures(file_list: [str]) -> [str]:
    pic_list = []
    for file in file_list:
        url = file["url"]
        query = parse.urlparse(url).query
        extra = parse.parse_qs(query)["extra"][0]
        request : DownloadMediaRequest = DownloadMediaRequest.builder() \
                .file_token(file["file_token"]) \
                .extra(extra) \
                .build()
        response : DownloadMediaResponse = await client.drive.v1.media.adownload(request)
        if not response.success():
            lark.logger.error(f"client.drive.v1.media.adownload failed, "
                             + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            raise RuntimeError(f"error_code: {response.code}", response)
        pic_path = pic_dir+file["name"]
        if save_pics:
            with open(pic_path, "wb") as f:
                f.write(response.file.read())
            pic_list.append(pic_path)
        else:
            pic_list.append(response.file.read())
    return pic_list

async def upload_pictures(pic_list: [str]) -> None:
    key_list = []
    for pic in pic_list:
        if save_pics:
            file = open(pic, "rb")
        else:
            file = io.BytesIO(pic)
        try:
            request : CreateImageRequest = CreateImageRequest.builder() \
                    .request_body(CreateImageRequestBody.builder()
                        .image_type("message") \
                        .image(file) \
                        .build()) \
                    .build()
            response : CreateImageResponse = await client.im.v1.image.acreate(request)
            if not response.success():
                lark.logger.error(f"client.im.v1.image.acreate failed, "
                                 + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
                raise RuntimeError(f"error_code: {response.code}", response)
        finally:
            file.close()
        global debug_item
        debug_item.append(response)
        key_list.append({"tag": "img", "image_key": response.data.image_key})
        lark.logger.info(f"[upload message picture] sent image key: {response.data.image_key}")
    return key_list

async def get_record(record_id: str, table_id:str):
    request : BatchGetAppTableRecordRequest = BatchGetAppTableRecordRequest.builder() \
            .app_token(file_token) \
            .table_id(table_id) \
            .request_body(BatchGetAppTableRecordRequestBody.builder()
                          .record_ids([record_id])
                          .automatic_fields(True)
                          .build()) \
            .build()
    response : BatchGetAppTableRecordResponse = await client.bitable.v1.app_table_record.abatch_get(request)
    if not response.success():
        lark.logger.error(f"client.bitable.v1.app_table_record.batch_get failed, "
                         + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        raise RuntimeError(f"error_code: {response.code}", response)

    #response_dict = lark.JSON.unmarshal(response.raw.content, dict)
    lark.logger.debug(f"[get_record access] data: {lark.JSON.marshal(response.data, indent=4)}")

    if not response.data.records:
        raise RuntimeError(f"cannot get record, record_id:{record_id} code:{response.code}", response)
    response_record = response.data.records[0]
    return response_record

async def send_message(title: str, content: object, msg_type:str):
    # sending message
    #message_obj = {"zh_cn":{"title": title, "content": [[{"tag":"text", "text": message}]]}}
    message_obj = {"zh_cn":{"title": title, "content": content}}
    print("Sending Message: \n", message)
    request : CreateMessageRequest = CreateMessageRequest.builder() \
            .receive_id_type(receive_id_type) \
            .request_body(CreateMessageRequestBody.builder()
                          .receive_id(receive_id)
                          .msg_type(msg_type)
                          .content(marshal(message_obj))
                          .build()) \
            .build()
    response : CreateMessageResponse = await client.im.v1.message.acreate(request)
    if not response.success():
        lark.logger.error(f"client.im.v1.message.create failed, "
                         + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        raise RuntimeError(f"error_code: {response.code}", response)

async def do_full_food_record_data(record_id: str) -> None:
    response_record = await get_record(record_id, table_id)
    record_value = response_record.fields
    record_string = {}
    for field, data in record_value.items():
        lark.logger.debug(f"{field}: {data}")

    for field in fields_by_name.keys():
        #record_value.setdefault(field, "")
        if field not in record_value:
            record_string[field] = ""
        else:
            record_string[field] = field_value_to_string(record_value[field], field_type=fields_by_name[field].type, field_property=fields_by_name[field].property)

    if record_string["餐次"] == "早餐":
        record_string["本餐应吃碳水"] = record_string["早餐应吃碳水"]
        record_string["本餐应吃蛋白质"] = record_string["早餐应吃蛋白质"]
        record_string["本餐应吃脂肪"] = record_string["早餐应吃脂肪"]
    elif record_string["餐次"] == "午餐":
        record_string["本餐应吃碳水"] = record_string["午餐应吃碳水"]
        record_string["本餐应吃蛋白质"] = record_string["午餐应吃蛋白质"]
        record_string["本餐应吃脂肪"] = record_string["午餐应吃脂肪"]
    elif record_string["餐次"] == "晚餐":
        record_string["本餐应吃碳水"] = record_string["晚餐应吃碳水"]
        record_string["本餐应吃蛋白质"] = record_string["晚餐应吃蛋白质"]
        record_string["本餐应吃脂肪"] = record_string["晚餐应吃脂肪"]
    else:
        record_string["本餐应吃碳水"] = record_string["晚餐应吃碳水"]
        record_string["本餐应吃蛋白质"] = record_string["晚餐应吃蛋白质"]
        record_string["本餐应吃脂肪"] = record_string["晚餐应吃脂肪"]

    message = message_template.format(**record_string)
    title = f'{record_value["创建人"][0]["name"]}饮食记录'

    global debug_item
    debug_item = [response_record, record_string, message]

    if "本餐照片" in record_value:
        # retrieve pictures
        pic_list = await retrieve_pictures(record_value["本餐照片"])

        # upload pictures
        key_list = await upload_pictures(pic_list)

        content = [key_list, split_message(message)]
    else:
        content = [split_message(message)]

    await send_message(title, content, "post")

async def do_full_exercise_record_data(record_id: str) -> None:
    response_record = await get_record(record_id, table1_id)
    record_value = response_record.fields
    record_string = {}
    for field, data in record_value.items():
        lark.logger.debug(f"{field}: {data}")

    for field in fields1_by_name.keys():
        #record_value.setdefault(field, "")
        if field not in record_value:
            record_string[field] = ""
        else:
            record_string[field] = field_value_to_string(record_value[field], field_type=fields1_by_name[field].type, field_property=fields1_by_name[field].property)

    message = message1_template.format(**record_string)
    title = f'{record_value["创建人"][0]["name"]}运动记录'

    global debug_item
    debug_item = [response_record, record_string, message]

    if "记录图片" in record_value:
        # retrieve pictures
        pic_list = await retrieve_pictures(record_value["记录图片"])

        # upload pictures
        key_list = await upload_pictures(pic_list)

        content = [key_list, split_message(message)]
    else:
        content = [split_message(message)]

    await send_message(title, content, "post")

def done_callback(task):
    global task_list
    if task.exception():
        lark.logger.error(f"Error occurred for task {task.get_name()}: {task.print_stack()}")
    else:
        task_list.discard(task)

def do_food_table_change(data: lark.drive.v1.P2DriveFileBitableRecordChangedV1) -> None:
    for record_action in data.event.action_list:
        lark.logger.info(f"[do_exercise_table_change access] action: {record_action.action}, record_id: {record_action.record_id}")
        if record_action.action == "record_added":
            record_value = record_action.after_value
        elif record_action.action == "record_edited":
            record_value = record_action.after_value
        elif record_action.action == "record_deleted":
            record_value = None
            continue
        lark.logger.debug(f"[do_food_table_change access] data:")
        for field in record_value:
            lark.logger.debug(f"{fields_by_id[field.field_id].field_name}: {field.field_value}")
        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(do_full_food_record_data(record_action.record_id))
            global task_list
            task_list.add(task)
            task.add_done_callback(done_callback)
        except RuntimeError as e:
            lark.logger.error(e)

def do_exercise_table_change(data: lark.drive.v1.P2DriveFileBitableRecordChangedV1) -> None:
    for record_action in data.event.action_list:
        lark.logger.info(f"[do_exercise_table_change access] action: {record_action.action}, record_id: {record_action.record_id}")
        if record_action.action == "record_added":
            record_value = record_action.after_value
        elif record_action.action == "record_edited":
            record_value = record_action.after_value
        elif record_action.action == "record_deleted":
            record_value = None
            continue
        lark.logger.debug(f"[do_exercise_table_change access] data:")
        for field in record_value:
            lark.logger.debug(f"{fields1_by_id[field.field_id].field_name}: {field.field_value}")
        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(do_full_exercise_record_data(record_action.record_id))
            global task_list
            task_list.add(task)
            task.add_done_callback(done_callback)
        except RuntimeError as e:
            lark.logger.error(e)

def check_duplicate(event_id: str)-> bool:
    global dedup_list
    global dedup_list_ptr
    if event_id in dedup_list:
        return True
    dedup_list[dedup_list_ptr] = event_id
    dedup_list_ptr = (dedup_list_ptr+1) % dedup_list_size
    return False

def do_record_change(data: lark.drive.v1.P2DriveFileBitableRecordChangedV1) -> None:
    global last_data
    last_data = data
    if check_duplicate(data.header.event_id):
        lark.logger.info(f"[do_record_change access] duplicate event ignored, event_id: {data.header.event_id}")
        return
    lark.logger.info(f"[do_record_change access] handle incoming event, event_id: {data.header.event_id}, table_id: {data.event.table_id}, revision: {data.event.revision}")
    lark.logger.debug(f"[do_record_change access] data:{lark.JSON.marshal(data, indent=4)}")
    handler = subscription_table.get(data.event.table_id, None)
    if handler:
        handler(data)

def get_tenant_access_token() -> str:
    request = InternalTenantAccessTokenRequest.builder() \
            .request_body(InternalTenantAccessTokenRequestBody.builder() \
                        .app_id(app_id) \
                        .app_secret(app_secret) \
                        .build()) \
            .build()
    response = client.auth.v3.tenant_access_token.internal(request)

    if not response.success():
        lark.logger.error(f"client.auth.v3.tenant_access_token.internal failed, "
                         + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        raise RuntimeError(f"error_code: {response.code}", response)

    response_dict = lark.JSON.unmarshal(response.raw.content, dict)
    lark.logger.debug(lark.JSON.marshal(response_dict, indent=4))
    return response_dict["tenant_access_token"]

def get_chats() -> dict:
    chat_dict = {}
    has_more = True
    page_token = ""
    while has_more:
        request : ListChatRequest = ListChatRequest.builder() \
                .page_token(page_token) \
                .page_size(20) \
                .build()

        response : ListChatResponse = client.im.v1.chat.list(request)
        if not response.success():
            lark.logger.error(f"client.im.v1.chat.list failed, "
                             + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            raise RuntimeError(f"error_code: {response.code}", response)

        lark.logger.debug(lark.JSON.marshal(response.data.items, indent=4))
        for chat in response.data.items:
            chat_dict[chat.name] = chat
        page_token = response.data.page_token
        has_more = response.data.has_more
    return chat_dict

def get_file_token(wiki_token: str) -> str:
    request : GetNodeSpaceRequest = GetNodeSpaceRequest.builder() \
            .token(wiki_token) \
            .obj_type("wiki") \
            .build()

    response : GetNodeSpaceResponse = client.wiki.v2.space.get_node(request)
    if not response.success():
        lark.logger.error(f"client.wiki.v2.space.get_node failed, "
                         + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        raise RuntimeError(f"error_code: {response.code}", response)

    response_node : node.Node = response.data.node
    if response_node.obj_type != "bitable":
        raise RuntimeError(f"Wrong object type: {response_node.obj_type}", response)

    lark.logger.debug(lark.JSON.marshal(response_node, indent=4))
    return response_node.obj_token

def get_table_ids(file_token: str) -> str:
    items = {}
    has_more = True
    page_token = ""

    while has_more:
        request : ListAppTableRequest = ListAppTableRequest.builder() \
                .app_token(file_token) \
                .page_token(page_token) \
                .page_size(20) \
                .build()

        response : ListAppTableResponse = client.bitable.v1.app_table.list(request)
        if not response.success():
            lark.logger.error(f"client.bitable.v1.app_table.list failed, "
                             + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            raise RuntimeError(f"error_code: {response.code}", response)

        response_data : list_app_table_response_body.ListAppTableResponseBody = response.data
        has_more = response_data.has_more
        page_token = response_data.page_token

        lark.logger.debug(lark.JSON.marshal(response.data, indent=4))
        for item in response_data.items:
            items[item.name] = item

    return items

def subscribe(file_token: str) -> bool:
    request : SubscribeFileRequest = SubscribeFileRequest.builder() \
            .file_token(file_token) \
            .file_type("bitable") \
            .build()

    response : SubscribeFileResponse = client.drive.v1.file.subscribe(request)
    if not response.success():
        lark.logger.error(f"client.drive.v1.file.subscribe failed, "
                         + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        raise RuntimeError(f"error_code: {response.code}", response)

    response_dict = lark.JSON.unmarshal(response.raw.content, dict)
    lark.logger.debug(lark.JSON.marshal(response_dict, indent=4))
    return response_dict["msg"] == "Success"

def check_subscription(file_token: str) -> bool: 
    request : GetSubscribeFileRequest = GetSubscribeFileRequest.builder() \
            .file_token(file_token) \
            .file_type("bitable") \
            .build()

    response : GetSubscribeFileResponse = client.drive.v1.file.get_subscribe(request)
    if not response.success():
        lark.logger.error(f"client.drive.v1.file.get_subscribe failed, "
                         + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        raise RuntimeError(f"error_code: {response.code}", response)

    response_dict = lark.JSON.unmarshal(response.raw.content, dict)
    lark.logger.debug(lark.JSON.marshal(response_dict, indent=4))
    return response_dict["data"]["is_subscribe"]

def get_fields(file_token: str, table_id: str) -> list[ListAppTableFieldResponse]: 
    fields = []
    has_more = True
    page_token = ""

    while has_more:
        request : ListAppTableFieldRequest = ListAppTableFieldRequest.builder() \
                .app_token(file_token) \
                .table_id(table_id) \
                .page_token(page_token) \
                .page_size(20) \
                .build()

        response : ListAppTableFieldResponse = client.bitable.v1.app_table_field.list(request)
        if not response.success():
            lark.logger.error(f"client.bitable.v1.app_table_field.list failed, "
                             + f"code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
            raise RuntimeError(f"error_code: {response.code}", response)

        response_data : list_app_table_field_response_body.ListAppTableFieldResponseBody = response.data
        has_more = response_data.has_more
        page_token = response_data.page_token
        response_dict = {item.field_id:item for item in response.data.items}
        lark.logger.debug(lark.JSON.marshal(response.data, indent=4))
        fields.extend(response_data.items)
        #for item in response_data.items:
        #    fields[item.field_name] = item

    return fields

def excepthook(args, /):
    if args.exc_type == SystemExit:
        return
    print(f"caught exception: exc_type:{args.exc_type}, exc_value:{args.exc_value}, exc_traceback:{args.exc_traceback}, thread:{args.thread}", file=sys.stderr)

async def run_ws_client() -> None:
    ws_client.start()

# build clients
event_handler = lark.EventDispatcherHandler.builder("", "") \
        .register_p2_drive_file_bitable_record_changed_v1(do_record_change) \
        .build()


client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(loglevel) \
        .build()

ws_client = lark.ws.Client(app_id, \
                           app_secret, \
                           event_handler=event_handler, \
                           log_level=loglevel)


if __name__ == "__main__":
    if not file_token and wiki_token:
        file_token = get_file_token(wiki_token)
    if not check_subscription(file_token):
        subscribe(file_token)

    if not receive_id and receive_name:
        chats_dict = get_chats()
        receive_id = chats_dict[receive_name].chat_id
    lark.logger.info(f"Message receiver group_id: {receive_id}")

    # get table ids
    table_ids = get_table_ids(file_token)
    table_id = table_ids[table_name].table_id
    table1_id = table_ids[table1_name].table_id

    # get fields in table
    fields_list = get_fields(file_token, table_id)
    fields_by_name = {field.field_name:field for field in fields_list}
    fields_by_id = {field.field_id:field for field in fields_list}
    fields1_list = get_fields(file_token, table1_id)
    fields1_by_name = {field.field_name:field for field in fields1_list}
    fields1_by_id = {field.field_id:field for field in fields1_list}

    # set listening table
    subscription_table[table_id] = do_food_table_change
    subscription_table[table1_id] = do_exercise_table_change

    # start subscription listening
    #loop = asyncio.get_event_loop()
    #ws_task = loop.create_task(run_ws_client)
    #atexit.register(lambda : asyncio.wait_for(ws_task, timeout=3.0))
    ws_thread = threading.Thread(target = ws_client.start)
    threading.excepthook = excepthook
    ws_thread.start()
    loop = asyncio.get_event_loop()

    #test for a specific record
    #task = loop.create_task(do_full_food_record_data(record_id))

    #run interactive console if not in interactive mode
    if not sys.flags.interactive and not hasattr(sys, "ps1"):
        code.InteractiveConsole(locals=globals()).interact()

