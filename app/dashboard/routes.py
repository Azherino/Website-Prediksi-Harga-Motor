import os
from flask import render_template, jsonify, send_file, current_app
from flask_login import login_required, current_user
from sqlalchemy import func
from app.dashboard import dashboard_bp
from app.models import MotorData, PrediksiHasil, ModelTraining, Dataset
from app.ml.report import shared_draw_header, _table_style

import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

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

@dashboard_bp.route('/download-report')
@login_required
def download_report():
    # ── Fetch Data ──────────────────────────────────────────────────────────
    merek_agg = (MotorData.query
                 .with_entities(MotorData.merek_motor, func.count(MotorData.id))
                 .group_by(MotorData.merek_motor).all())
    merek_labels = [r[0] for r in merek_agg]
    merek_counts = [r[1] for r in merek_agg]

    avg_merek = (MotorData.query
                 .with_entities(MotorData.merek_motor, func.avg(MotorData.harga_aktual))
                 .group_by(MotorData.merek_motor).all())
    avg_labels = [r[0] for r in avg_merek]
    avg_values = [int(r[1]) for r in avg_merek]

    latest_preds = (PrediksiHasil.query
                    .order_by(PrediksiHasil.created_at.desc())
                    .limit(15).all())

    # ── Chart 1: Distribusi ──────────────────────────────────────────────────
    plt.figure(figsize=(6, 4))
    plt.bar(merek_labels, merek_counts, color='#4CAF50')
    plt.title('Distribusi Motor per Merek')
    plt.xlabel('Merek')
    plt.ylabel('Jumlah')
    plt.xticks(rotation=45)
    plt.tight_layout()
    img_dist = io.BytesIO()
    plt.savefig(img_dist, format='png', dpi=150)
    img_dist.seek(0)
    plt.close()

    # ── Chart 2: Rata-rata ──────────────────────────────────────────────────
    plt.figure(figsize=(6, 4))
    plt.bar(avg_labels, avg_values, color='#2196F3')
    plt.title('Rata-rata Harga per Merek')
    plt.xlabel('Merek')
    plt.ylabel('Harga (Rp)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    img_avg = io.BytesIO()
    plt.savefig(img_avg, format='png', dpi=150)
    img_avg.seek(0)
    plt.close()

    # ── Chart 3: Aktual vs Prediksi ──────────────────────────────────────────
    last_model = ModelTraining.query.order_by(ModelTraining.created_at.desc()).first()
    aktual_list = []
    prediksi_list = []
    if last_model and last_model.y_test_data and last_model.y_pred_data:
        aktual_list   = [int(v) for v in last_model.y_test_data[:20]]
        prediksi_list = [int(v) for v in last_model.y_pred_data[:20]]
    
    img_aktual_pred = None
    if aktual_list and prediksi_list:
        plt.figure(figsize=(6, 4))
        plt.plot(range(1, len(aktual_list) + 1), aktual_list, label='Aktual', marker='o', color='#4CAF50')
        plt.plot(range(1, len(prediksi_list) + 1), prediksi_list, label='Prediksi', marker='x', linestyle='--', color='#2196F3')
        plt.title('Perbandingan Harga Aktual vs Prediksi (Data Test Terakhir)')
        plt.xlabel('Data ke-')
        plt.ylabel('Harga (Rp)')
        plt.legend()
        plt.tight_layout()
        img_aktual_pred = io.BytesIO()
        plt.savefig(img_aktual_pred, format='png', dpi=150)
        img_aktual_pred.seek(0)
        plt.close()

    # ── PDF Generation ───────────────────────────────────────────────────────
    pdf_buffer = io.BytesIO()
    # Tingkatkan topMargin agar konten tidak menabrak header
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=90, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = 1

    # Page 1
    elements.append(Paragraph("Laporan Dashboard Analisis", title_style))
    elements.append(Paragraph(f"Dicetak pada: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("1. Grafik Distribusi Motor per Merek", styles['Heading2']))
    elements.append(RLImage(img_dist, width=5.5*inch, height=3.6*inch))
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("2. Grafik Rata-rata Harga per Merek", styles['Heading2']))
    elements.append(RLImage(img_avg, width=5.5*inch, height=3.6*inch))
    
    # Page 2
    elements.append(PageBreak())
    
    if img_aktual_pred:
        elements.append(Paragraph("3. Grafik Perbandingan Harga Aktual vs Prediksi", styles['Heading2']))
        elements.append(RLImage(img_aktual_pred, width=5.5*inch, height=3.6*inch))
        elements.append(Spacer(1, 15))
        # Jika grafik 3 ada, tambahkan PageBreak lagi agar tabel tidak terpotong dengan grafik
        elements.append(PageBreak())

    elements.append(Paragraph("Hasil Prediksi Terbaru", title_style))
    elements.append(Spacer(1, 20))

    data_table = [['No', 'Merek', 'Tipe', 'Tahun', 'Jarak (km)', 'Kondisi', 'Harga Prediksi']]
    for i, p in enumerate(latest_preds, 1):
        data_table.append([
            str(i),
            p.merek_motor,
            p.tipe_motor,
            str(p.tahun_produksi),
            f"{int(p.jarak_tempuh):,}".replace(',', '.'),
            p.kondisi_fisik,
            f"Rp {p.harga_prediksi:,}".replace(',', '.')
        ])
    
    t = Table(data_table, colWidths=[25, 60, 110, 40, 70, 70, 100])
    base_style = _table_style()
    base_style.add('ALIGN', (0, 0), (-1, 0), 'CENTER')
    base_style.add('ALIGN', (0, 1), (0, -1), 'CENTER')
    base_style.add('ALIGN', (3, 1), (3, -1), 'CENTER')
    base_style.add('ALIGN', (4, 1), (4, -1), 'RIGHT')
    base_style.add('ALIGN', (6, 1), (6, -1), 'RIGHT')
    t.setStyle(base_style)
    elements.append(t)

    doc.build(elements, onFirstPage=shared_draw_header, onLaterPages=shared_draw_header)
    pdf_buffer.seek(0)

    filename = f"Laporan_Prediksi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(pdf_buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')
