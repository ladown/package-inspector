"""
Flask приложение Package Inspector
"""
import os
from flask import Flask
from flask_cors import CORS


def create_app():
    """Фабрика для создания Flask приложения"""

    # Определяем пути относительно backend директории
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.path.dirname(backend_dir)

    # Создаем Flask приложение с настройкой путей к шаблонам и статике
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, 'frontend', 'templates'),
        static_folder=os.path.join(project_root, 'frontend', 'static')
    )

    # Загружаем конфигурацию
    app.config.from_object('app.config.Config')

    # Настраиваем CORS для работы с фронтендом
    CORS(app)

    # Создаем директорию uploads если не существует
    uploads_dir = os.path.join(backend_dir, app.config['UPLOAD_FOLDER'])
    os.makedirs(uploads_dir, exist_ok=True)

    # Регистрируем routes
    from app import routes
    app.register_blueprint(routes.bp)

    return app
