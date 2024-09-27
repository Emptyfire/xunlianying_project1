# run.py
from app import create_app


app = create_app()

if __name__ == "__main__":
    # 启动 Flask 应用
    app.run(port= 7777)
