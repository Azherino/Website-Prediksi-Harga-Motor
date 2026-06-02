from flask import Blueprint
prediksi_bp = Blueprint('prediksi', __name__, url_prefix='/prediksi')
from app.prediksi import routes  # noqa
