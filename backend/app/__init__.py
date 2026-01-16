import os

from flask import Flask
from flask_cors import CORS


def create_app():
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.path.dirname(backend_dir)

    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "frontend", "templates"),
        static_folder=os.path.join(project_root, "frontend", "static"),
    )

    app.config.from_object("app.config.Config")

    CORS(app)

    uploads_dir = os.path.join(backend_dir, app.config["UPLOAD_FOLDER"])
    os.makedirs(uploads_dir, exist_ok=True)

    from app import routes

    app.register_blueprint(routes.bp)

    return app
