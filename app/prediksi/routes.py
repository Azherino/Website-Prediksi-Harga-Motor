import os
from flask import (render_template, redirect, url_for, flash,
                   request, current_app, send_file, jsonify)
from flask_login import login_required, current_user
from app.prediksi import prediksi_bp
from app.models import Dataset, MotorData, ModelTraining, PrediksiHasil
from app import db
from app.ml.regression import train_model, predict_single
from app.ml.report import (generate_koefisien_pdf,
                            generate_prediksi_pdf,
                            generate_semua_prediksi_pdf)


@prediksi_bp.route('/training', methods=['GET', 'POST'])
@login_required
def training():
    datasets = Dataset.query.filter_by(status='valid').order_by(Dataset.created_at.desc()).all()

    if request.method == 'POST':
        dataset_id  = request.form.get('dataset_id', type=int)
        rasio_train = request.form.get('rasio_train', 80, type=int) / 100.0

        dataset = Dataset.query.get_or_404(dataset_id)
        motor_data = MotorData.query.filter_by(dataset_id=dataset_id).all()

        if len(motor_data) < 10:
            flash('Data terlalu sedikit untuk training (minimal 10 baris).', 'danger')
            return redirect(url_for('prediksi.training'))

        # Path for saving the trained model file
        model_fname = f"model_{dataset_id}_{int(rasio_train*100)}.pkl"
        model_path  = os.path.join(current_app.config['MODEL_FOLDER'], model_fname)

        try:
            result = train_model(motor_data, rasio_train=rasio_train,
                                 model_save_path=model_path)
        except Exception as e:
            flash(f'Gagal training model: {e}', 'danger')
            return redirect(url_for('prediksi.training'))

        mt = ModelTraining(
            dataset_id  = dataset_id,
            rasio_train = rasio_train,
            koefisien   = result['coefficients'],
            intercept   = result['intercept'],
            model_path  = model_path,
            r2_score    = result['r2'],
            mae         = result['mae'],
            mse         = result['mse'],
            rmse        = result['rmse'],
            mape        = result['mape'],
            train_size  = result['train_size'],
            test_size   = result['test_size'],
            y_test_data = result['y_test'],
            y_pred_data = result['y_pred'],
            trained_by  = current_user.id,
        )
        db.session.add(mt)
        db.session.commit()

        flash(f'Training selesai! R² = {result["r2"]:.4f}', 'success')
        return redirect(url_for('evaluasi.index'))

    return render_template('prediksi/training.html', datasets=datasets)


@prediksi_bp.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    models = ModelTraining.query.order_by(ModelTraining.created_at.desc()).all()

    if request.method == 'POST':
        model_id = request.form.get('model_id', type=int)
        model    = ModelTraining.query.get_or_404(model_id)

        if not os.path.exists(model.model_path):
            flash('File model tidak ditemukan. Silakan lakukan training ulang.', 'danger')
            return redirect(url_for('prediksi.form'))

        input_data = {
            'tahun_produksi':    request.form.get('tahun_produksi', type=int),
            'kapasitas_mesin':   request.form.get('kapasitas_mesin', type=float),
            'jarak_tempuh':      request.form.get('jarak_tempuh', type=float),
            'merek_motor':       request.form.get('merek_motor'),
            'kondisi_fisik':     request.form.get('kondisi_fisik'),
            'tipe_motor':        request.form.get('tipe_motor'),
            'model_motor':       request.form.get('model_motor'),
            'kelengkapan_surat': request.form.get('kelengkapan_surat'),
            'pajak':             request.form.get('pajak'),
        }

        try:
            harga = predict_single(model.model_path, input_data)
        except Exception as e:
            flash(f'Prediksi gagal: {e}', 'danger')
            return redirect(url_for('prediksi.form'))

        hasil = PrediksiHasil(
            model_id          = model_id,
            tahun_produksi    = input_data['tahun_produksi'],
            kapasitas_mesin   = input_data['kapasitas_mesin'],
            jarak_tempuh      = input_data['jarak_tempuh'],
            merek_motor       = input_data['merek_motor'],
            kondisi_fisik     = input_data['kondisi_fisik'],
            tipe_motor        = input_data['tipe_motor'],
            model_motor       = input_data['model_motor'],
            kelengkapan_surat = input_data['kelengkapan_surat'],
            pajak             = input_data['pajak'],
            harga_prediksi    = int(harga),
            predicted_by      = current_user.id,
        )
        db.session.add(hasil)
        db.session.commit()

        flash(f'Prediksi berhasil! Harga Estimasi: Rp {int(harga):,}'.replace(',', '.'), 'success')
        return redirect(url_for('prediksi.detail', prediksi_id=hasil.id))

    return render_template('prediksi/form.html', models=models)


@prediksi_bp.route('/hasil')
@login_required
def hasil():
    search   = request.args.get('q', '')
    merek_f  = request.args.get('merek', '')
    tipe_f   = request.args.get('tipe', '')
    page     = request.args.get('page', 1, type=int)

    query = PrediksiHasil.query
    if merek_f:
        query = query.filter(PrediksiHasil.merek_motor == merek_f)
    if tipe_f:
        query = query.filter(PrediksiHasil.tipe_motor == tipe_f)

    results  = query.order_by(PrediksiHasil.created_at.desc()).paginate(page=page, per_page=15)

    # Filter options
    mereks = db.session.query(PrediksiHasil.merek_motor).distinct().all()
    tipes  = db.session.query(PrediksiHasil.tipe_motor).distinct().all()

    return render_template('prediksi/hasil.html',
                           results=results,
                           mereks=[r[0] for r in mereks],
                           tipes=[r[0] for r in tipes],
                           merek_f=merek_f, tipe_f=tipe_f)


@prediksi_bp.route('/detail/<int:prediksi_id>')
@login_required
def detail(prediksi_id):
    p = PrediksiHasil.query.get_or_404(prediksi_id)
    return render_template('prediksi/detail.html', p=p)


@prediksi_bp.route('/hapus/<int:prediksi_id>', methods=['POST'])
@login_required
def hapus(prediksi_id):
    p = PrediksiHasil.query.get_or_404(prediksi_id)
    db.session.delete(p)
    db.session.commit()
    flash('Data prediksi berhasil dihapus.', 'success')
    return redirect(url_for('prediksi.hasil'))


@prediksi_bp.route('/report/<int:prediksi_id>/<string:fmt>')
@login_required
def report_prediksi(prediksi_id, fmt):
    p         = PrediksiHasil.query.get_or_404(prediksi_id)
    rdir      = current_app.config['REPORT_FOLDER']
    fname     = f"prediksi_report_{prediksi_id}.pdf"
    save_path = os.path.join(rdir, fname)
    generate_prediksi_pdf(p, current_user.nama, save_path)
    return send_file(save_path, mimetype='application/pdf',
                     as_attachment=True, download_name=fname)


@prediksi_bp.route('/report-koefisien/<int:model_id>')
@login_required
def report_koefisien(model_id):
    model     = ModelTraining.query.get_or_404(model_id)
    rdir      = current_app.config['REPORT_FOLDER']
    fname     = f"koefisien_report_{model_id}.pdf"
    save_path = os.path.join(rdir, fname)
    generate_koefisien_pdf(model, save_path)
    return send_file(save_path, mimetype='application/pdf',
                     as_attachment=True, download_name=fname)


@prediksi_bp.route('/report-semua')
@login_required
def report_semua():
    merek_f = request.args.get('merek', '')
    tipe_f  = request.args.get('tipe', '')

    query = PrediksiHasil.query
    if merek_f:
        query = query.filter(PrediksiHasil.merek_motor == merek_f)
    if tipe_f:
        query = query.filter(PrediksiHasil.tipe_motor == tipe_f)

    results = query.order_by(PrediksiHasil.created_at.desc()).all()

    rdir      = current_app.config['REPORT_FOLDER']
    fname     = "riwayat_prediksi_report.pdf"
    save_path = os.path.join(rdir, fname)

    generate_semua_prediksi_pdf(results, current_user.nama, save_path, merek_f=merek_f, tipe_f=tipe_f)
    return send_file(save_path, mimetype='application/pdf',
                     as_attachment=True, download_name=fname)

