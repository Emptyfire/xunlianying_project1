# run.py
from app import create_app
from app.client import start_lark_client
import threading

app = create_app()

if __name__ == "__main__":
    # 启动 Flask 应用
    threading.Thread(target=lambda: app.run(port=5000)).start()
    # 在新线程中启动 Lark 客户端
    threading.Thread(target=start_lark_client).start()