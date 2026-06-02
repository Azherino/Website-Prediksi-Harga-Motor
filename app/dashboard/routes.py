from flask import render_template, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from app.dashboard import dashboard_bp
from app.models import MotorData, PrediksiHasil, ModelTraining, Dataset


@dashboard_bp.route('/')
@login_required
def index():
    # ── Stats cards ──────────────────────────────────────────────────────────
    total_motor    = MotorData.query.count()
    total_prediksi = PrediksiHasil.query.count()

    last_model = ModelTraining.query.order_by(ModelTraining.created_at.desc()).first()
    r2_score   = round(last_model.r2_score * 100, 2) if last_model else 0

    avg_prediksi = 0
    if total_prediksi:
        avg_raw = PrediksiHasil.query.with_entities(
            func.avg(PrediksiHasil.harga_prediksi)).scalar()
        avg_prediksi = int(avg_raw or 0)

    # ── Latest predictions table ─────────────────────────────────────────────
    latest = (PrediksiHasil.query
              .order_by(PrediksiHasil.created_at.desc())
              .limit(5).all())

    # ── Chart: price distribution labels (merek) ─────────────────────────────
    merek_agg = (MotorData.query
                 .with_entities(MotorData.merek_motor, func.count(MotorData.id))
                 .group_by(MotorData.merek_motor).all())
    merek_labels = [r[0] for r in merek_agg]
    merek_counts = [r[1] for r in merek_agg]

    # ── Chart: avg price per merek ────────────────────────────────────────────
    avg_merek = (MotorData.query
                 .with_entities(MotorData.merek_motor,
                                func.avg(MotorData.harga_aktual).label('avg_h'))
                 .group_by(MotorData.merek_motor).all())
    avg_labels = [r[0] for r in avg_merek]
    avg_values = [int(r[1]) for r in avg_merek]

    # ── Chart: aktual vs prediksi (last model test data) ─────────────────────
    aktual_list = []
    prediksi_list = []
    if last_model and last_model.y_test_data and last_model.y_pred_data:
        aktual_list   = [int(v) for v in last_model.y_test_data[:20]]
        prediksi_list = [int(v) for v in last_model.y_pred_data[:20]]

    return render_template('dashboard/index.html',
        total_motor=total_motor,
        total_prediksi=total_prediksi,
        r2_score=r2_score,
        avg_prediksi=avg_prediksi,
        latest=latest,
        merek_labels=merek_labels,
        merek_counts=merek_counts,
        avg_labels=avg_labels,
        avg_values=avg_values,
        aktual_list=aktual_list,
        prediksi_list=prediksi_list,
    )
