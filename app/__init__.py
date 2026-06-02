from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silakan login terlebih dahulu.'
login_manager.login_message_category = 'warning'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure required directories exist
    for folder in [app.config['UPLOAD_FOLDER'],
                   app.config['MODEL_FOLDER'],
                   app.config['REPORT_FOLDER']]:
        os.makedirs(folder, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.auth    import auth_bp
    from app.dashboard import dashboard_bp
    from app.users   import users_bp
    from app.dataset import dataset_bp
    from app.prediksi import prediksi_bp
    from app.evaluasi import evaluasi_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(dataset_bp)
    app.register_blueprint(prediksi_bp)
    app.register_blueprint(evaluasi_bp)

    return app
