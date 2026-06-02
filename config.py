import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pt-putra-hamid-2024-secret'
    
    # MySQL connection — sesuaikan user/password/dbname Anda
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:@localhost/prediksi_motor'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER  = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MODEL_FOLDER   = os.path.join(BASE_DIR, 'app', 'static', 'models')
    REPORT_FOLDER  = os.path.join(BASE_DIR, 'app', 'static', 'reports')
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024   # 32 MB
