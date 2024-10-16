#/feishu/var_db.py

import json

# 令牌

# 启动参数
app_id = "cli_a67b17d72e7a900b"
app_secret = "4XVYaGd04umVor0oSjrkicEeeKKqH125"


# 表字段引用
wiki_token = ""
file_token = ""
table_name = ""
table1_name = ""
receive_name = ""
receive_id = ""
receive_id_type = "chat_id"

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

# marshal = lark.JSON.marshal
# unmarshal = lark.JSON.unmarshal
# dedup_list = [""]*dedup_list_size
# dedup_list_ptr = 0

subscription_table = {}


# debug
debug_item = None
task_list = set()

message_template = ""

