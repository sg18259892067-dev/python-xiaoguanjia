from flask import Flask
from app.config import Config
from app.database import init_db


def create_app():
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)

    # 先导入 models（注册到 Base）
    from app.models import user

    # 初始化数据库
    init_db(app)

    # 导入认证蓝图和 bcrypt
    from app.api.auth import auth_bp, bcrypt

    # 初始化 bcrypt
    bcrypt.init_app(app)

    # 注册蓝图
    app.register_blueprint(auth_bp)

    # 健康检查接口
    @app.route("/")
    def health():
        return {"status": "running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
