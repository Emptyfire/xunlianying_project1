from feishu.means import uget_tenant_access_token
from feishu.means import uget_record
from feishu.means import usend_message
from feishu.means import get_json
from feishu.card_config import card
import json
import lark_oapi as lark
from _thread import _excepthook, _ExceptHookArgs, get_native_id as get_native_id
import threading, asyncio
import pprint

#data = get_json(card)
#data =  "{\"type\":\"template\",\"data\":{\"template_id\":\"AAq7B3J2NUFv8\",\"template_version_name\":\"1.0.0\",\"template_variable\":{\"group_name\":\"A组\",\"name\":\"绝望的肉\",\"tree\":\"午餐\",\"record\":\"1\"}}}"
#print(data)
p = uget_record()
print(p)

#r = json.loads(data)
#print('json转字典:{} type:{}'.format(r, type(r)))
