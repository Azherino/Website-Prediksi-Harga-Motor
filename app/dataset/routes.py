import os
import uuid
import pandas as pd
from flask import (render_template, redirect, url_for, flash,
                   request, current_app, send_file)
from flask_login import login_required, current_user
from app.dataset import dataset_bp
from app.models import Dataset, MotorData
from app import db
from app.ml.preprocessing import validate_columns, normalize_columns, get_dataset_stats
from app.ml.report import generate_dataset_pdf, generate_dataset_excel

ALLOWED = {'csv', 'xlsx', 'xls'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED


@dataset_bp.route('/')
@login_required
def index():
    datasets = Dataset.query.order_by(Dataset.created_at.desc()).all()
    return render_template('dataset/index.html', datasets=datasets)


@dataset_bp.route('/import', methods=['GET', 'POST'])
@login_required
def import_dataset():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Tidak ada file yang dipilih.', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Tidak ada file yang dipilih.', 'danger')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Format file tidak didukung. Gunakan CSV atau Excel.', 'danger')
            return redirect(request.url)

        # Save file
        ext       = file.filename.rsplit('.', 1)[1].lower()
        safe_name = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_name)
        file.save(save_path)

        # Parse — auto-detect baris header yang benar
        try:
            if ext == 'csv':
                df = pd.read_csv(save_path)
            else:
                # Coba baca dengan berbagai header row (0-5)
                # Pilih yang paling banyak cocok dengan kolom yang dibutuhkan
                from app.ml.preprocessing import COLUMN_ALIASES
                all_aliases = set()
                for aliases in COLUMN_ALIASES.values():
                    for a in aliases:
                        all_aliases.add(a.strip().lower())

                best_df        = None
                best_match     = -1
                for header_row in range(6):
                    try:
                        tmp = pd.read_excel(save_path, header=header_row)
                        cols_lower = [str(c).strip().lower() for c in tmp.columns]
                        match = sum(1 for c in cols_lower if c in all_aliases)
                        if match > best_match:
                            best_match = match
                            best_df    = tmp
                    except Exception:
                        continue
                df = best_df if best_df is not None else pd.read_excel(save_path)
        except Exception as e:
            os.remove(save_path)
            flash(f'Gagal membaca file: {e}', 'danger')
            return redirect(request.url)

        # Normalisasi & validasi kolom
        df = normalize_columns(df)

        # Hapus kolom 'No' / nomor urut jika ada
        no_cols = [c for c in df.columns if str(c).strip().lower() in ('no', 'no.', 'nomor', '#')]
        if no_cols:
            df = df.drop(columns=no_cols)

        # Hapus baris yang isinya adalah teks header (duplikat header di tengah data)
        if 'tahun_produksi' in df.columns:
            df = df[df['tahun_produksi'].astype(str).str.lower() != 'tahun produksi']
            df = df[pd.to_numeric(df['tahun_produksi'], errors='coerce').notna()]

        df = df.reset_index(drop=True)

        missing = validate_columns(df)
        status  = 'invalid' if missing else 'valid'

        # DEBUG: tampilkan kolom yang terbaca
        import logging
        logging.warning(f"[DEBUG] Kolom terbaca dari file: {list(df.columns)}")
        logging.warning(f"[DEBUG] Kolom yang hilang: {missing}")

        dataset = Dataset(
            nama_file   = file.filename,
            path_file   = save_path,
            jumlah_data = len(df),
            status      = status,
            uploaded_by = current_user.id,
        )
        db.session.add(dataset)
        db.session.flush()   # get dataset.id

        if status == 'valid':
            # Save motor data rows
            has_model = 'model_motor' in df.columns
            for _, row in df.iterrows():
                md = MotorData(
                    dataset_id        = dataset.id,
                    tahun_produksi    = int(row['tahun_produksi']),
                    kapasitas_mesin   = float(row['kapasitas_mesin']),
                    jarak_tempuh      = float(row['jarak_tempuh']),
                    merek_motor       = str(row['merek_motor']),
                    kondisi_fisik     = str(row['kondisi_fisik']),
                    tipe_motor        = str(row['tipe_motor']),
                    model_motor       = str(row['model_motor']) if has_model else None,
                    kelengkapan_surat = str(row['kelengkapan_surat']),
                    pajak             = str(row['pajak']),
                    harga_aktual      = int(row['harga_aktual']),
                )
                db.session.add(md)
            db.session.commit()
            flash(f'Dataset berhasil diimport: {len(df)} data.', 'success')
            return redirect(url_for('dataset.preview', dataset_id=dataset.id))
        else:
            db.session.commit()
            flash(f'Dataset invalid — kolom tidak ditemukan: {", ".join(missing)}', 'danger')
            return redirect(url_for('dataset.index'))

    return render_template('dataset/import.html')


@dataset_bp.route('/preview/<int:dataset_id>')
@login_required
def preview(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    try:
        ext = dataset.path_file.rsplit('.', 1)[1].lower()
        df  = pd.read_csv(dataset.path_file) if ext == 'csv' else pd.read_excel(dataset.path_file)
    except Exception:
        df = None

    stats   = get_dataset_stats(df) if df is not None else {}
    preview = df.head(10).to_dict(orient='records') if df is not None else []
    columns = list(df.columns) if df is not None else []
    missing_vals = df.isnull().sum().to_dict() if df is not None else {}

    return render_template('dataset/preview.html',
                           dataset=dataset, preview=preview,
                           columns=columns, stats=stats,
                           missing_vals=missing_vals,
                           total_rows=len(df) if df is not None else 0)


@dataset_bp.route('/hapus/<int:dataset_id>', methods=['POST'])
@login_required
def hapus(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    try:
        if os.path.exists(dataset.path_file):
            os.remove(dataset.path_file)
    except Exception:
        pass
    db.session.delete(dataset)
    db.session.commit()
    flash('Dataset berhasil dihapus.', 'success')
    return redirect(url_for('dataset.index'))


@dataset_bp.route('/report/<int:dataset_id>/<string:fmt>')
@login_required
def report(dataset_id, fmt):
    dataset = Dataset.query.get_or_404(dataset_id)
    ext     = dataset.path_file.rsplit('.', 1)[1].lower()
    try:
        df = pd.read_csv(dataset.path_file) if ext == 'csv' else pd.read_excel(dataset.path_file)
    except Exception as e:
        flash(f'Gagal membaca file: {e}', 'danger')
        return redirect(url_for('dataset.preview', dataset_id=dataset_id))

    stats     = get_dataset_stats(df)
    rdir      = current_app.config['REPORT_FOLDER']
    fname     = f"dataset_report_{dataset_id}.{fmt}"
    save_path = os.path.join(rdir, fname)

    if fmt == 'pdf':
        generate_dataset_pdf(dataset, stats, save_path)
        mime = 'application/pdf'
    else:
        generate_dataset_excel(dataset, stats, save_path)
        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    return send_file(save_path, mimetype=mime, as_attachment=True,
                     download_name=fname)
