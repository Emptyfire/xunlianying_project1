# Readme

本项目为训练营数据获取项目相关

### 已完成项

现在于飞书的开发者平台中,选择使用长连接模式,建立连接后可正常接收文本变更事件,能够返回变更后的 json

> 回传 json 已加密,需要进行解码,解码参阅飞书教程
> https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/event-subscription-guide/callback-subscription/receive-and-handle-callbacks

### 路由解释

- http://127.0.0.1:5000/ 为初始欢迎页面
- http://127.0.0.1:5000/event 为启动飞书 sdk 的长连接客户端

启动本地 flask 客户端后,访问指定路径即可
