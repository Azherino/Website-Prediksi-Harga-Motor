from flask import Blueprint
evaluasi_bp = Blueprint('evaluasi', __name__, url_prefix='/evaluasi')
from app.evaluasi import routes  # noqa
