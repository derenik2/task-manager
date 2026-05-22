import os
from flask import Flask
from .extensions import db
from config import config_map


def create_app(env: str | None = None) -> Flask:
    if env is None:
        env = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config_map[env])

    db.init_app(app)

    from .routes.tasks import tasks_bp
    from .routes.users import users_bp

    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(users_bp, url_prefix="/users")

    with app.app_context():
        db.create_all()

    return app
