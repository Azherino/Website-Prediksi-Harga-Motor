import os
from flask import (render_template, redirect, url_for, flash,
                   request, current_app, send_file)
from flask_login import login_required
from app.evaluasi import evaluasi_bp
from app.models import ModelTraining
from app.ml.report import generate_evaluasi_pdf, generate_evaluasi_excel


@evaluasi_bp.route('/')
@login_required
def index():
    models = ModelTraining.query.order_by(ModelTraining.created_at.desc()).all()
    active = request.args.get('model_id', type=int)
    if not active and models:
        active = models[0].id
    model = ModelTraining.query.get(active) if active else None
    return render_template('evaluasi/index.html', models=models,
                           model=model, active_id=active)


@evaluasi_bp.route('/report/<int:model_id>/<string:fmt>')
@login_required
def report(model_id, fmt):
    model     = ModelTraining.query.get_or_404(model_id)
    rdir      = current_app.config['REPORT_FOLDER']
    fname     = f"evaluasi_report_{model_id}.{fmt}"
    save_path = os.path.join(rdir, fname)

    if fmt == 'pdf':
        generate_evaluasi_pdf(model, save_path)
        mime = 'application/pdf'
    else:
        generate_evaluasi_excel(model, save_path)
        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    return send_file(save_path, mimetype=mime,
                     as_attachment=True, download_name=fname)
