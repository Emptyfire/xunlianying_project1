# 目录结构说明

本文档旨在描述项目目录结构，以便开发者和维护人员能够更好地理解项目组织方式.

## 根目录

- `.vscode`：存放 Visual Studio Code 编辑器的配置文件和工作区设置.
- `app`：应用程序的主要代码目录
  - `__init__.py`：使 `app` 目录成为一个 Python 包.
  - `feishu`：包含与飞书（Feishu）API 交互相关的模块.
    - `data_download.py`：负责下载飞书数据的模块.
    - `event_listening.py`：处理飞书事件监听的模块.
    - `send_message_card.py`：发送消息卡片的模块.
  - `routes.py`：定义应用程序路由和视图函数.
  - `config`：存放配置文件的目录.
  - `templates`：存放相关模板文件, json 卡片模板等
  - `test`：包含测试代码和测试用例的目录.
  - `venv`：Python 虚拟环境目录，包含项目依赖.
- `.env`：存放环境变量的文件.
- `.gitignore`：指定 Git 忽略跟踪的文件和目录.
- `目录结构说明.md`：当前文件，描述目录结构.
- `run.py`：应用程序的启动脚本.

## 注意事项

1. 所有敏感信息，如 API 密钥和密码，应存储在 `.env` 文件中，并在 `.gitignore` 中排除.
2. `venv` 目录不应被提交到版本控制系统，以避免不同开发环境之间的依赖冲突.
3. `.vscode` 目录中的文件是 Visual Studio Code 编辑器的配置文件，不会影响到应用程序的运行.
4. `Include`、`Lib` 和 `Scripts` 目录的用途可能会根据项目需求而变化.
