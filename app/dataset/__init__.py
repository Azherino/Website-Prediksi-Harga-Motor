from flask import Blueprint
dataset_bp = Blueprint('dataset', __name__, url_prefix='/dataset')
from app.dataset import routes  # noqa
