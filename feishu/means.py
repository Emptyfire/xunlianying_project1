#feishu/means.py
import json,requests
import lark_oapi as lark
from feishu.var_db import app_id,app_secret,message_template

head = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer t-g104aga4OVGR2EN4T5KRKAZUQGZMZAPFRRFZ7O77'
        }


def get_json(data):
    str = json.dumps(data)
    return str

def response_structure(url,data,head):
    response = requests.post(url,data=data,headers=head)
    response_json = response.json()

    return response_json

def uget_tenant_access_token():
   return response_structure(
       "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
       data=json.dumps({ "app_id": app_id,"app_secret":app_secret}),head={"Content-Type":"application/json; charset=utf-8"}
)

def uget_record():
    return response_structure("https://open.feishu.cn/open-apis/bitable/v1/apps/SDlJwP51EiQH1ikJGJKcEazhnic/tables/tblzFl7WO11aJIRM/records/search"
                       ,data= json.dumps(
                           {
	                            "view_id": "vewrPkiodd",
                                "field_names": [
                                    "创建人",
                                    "分组",
                                    "餐次",
                                    "最新体重"
                                    ],
                                "automatic_fields": False
                           }
                       ),
                       head=head
    )

def usend_message(data):
    return response_structure(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        data=json.dumps(
            {
                "receive_id": "oc_151d83a170d782a087e6f3b33634cc01",
                "msg_type": "interactive",
                "content": data
            }
        ),
        head=head
    )

