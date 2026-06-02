# 🏍️ Sistem Prediksi Harga Motor Bekas — PT Putra Hamid

Membangun aplikasi web full-stack untuk memprediksi harga motor bekas menggunakan metode **Regresi Linear Berganda** (Multiple Linear Regression). Sistem ini digunakan oleh admin PT Putra Hamid untuk melakukan data mining terhadap dataset motor bekas, melatih model ML, dan menghasilkan prediksi harga.

---

## User Review Required

> [!IMPORTANT]
> **Tech Stack yang Akan Digunakan:**
> - **Backend:** Python + Flask (REST API)
> - **Frontend:** HTML + CSS + JavaScript (Vanilla, tanpa framework berat)
> - **Database:** SQLite (untuk kemudahan setup lokal, bisa migrasi ke MySQL/PostgreSQL)
> - **ML:** scikit-learn (LinearRegression), pandas, numpy
> - **Charts:** Chart.js (visualisasi di frontend)
> - **PDF Export:** ReportLab (Python)
> - **Excel Export:** openpyxl (Python)
>
> Apakah stack ini sudah sesuai dengan kebutuhan TA Anda?

> [!WARNING]
> **Scope yang Akan Dibangun (Semua Fase):**
> Karena ini adalah proyek Tugas Akhir yang lengkap, saya akan membangun **semua 6 fase** sesuai checklist di markdown. Proses ini akan menghasilkan cukup banyak file. Apakah Anda setuju?

> [!NOTE]
> **Autentikasi:** Menggunakan session Flask (server-side session) + bcrypt untuk hash password. Admin default akan dibuat otomatis saat setup pertama kali (username: `admin`, password: `admin123`).

---

## Open Questions

> [!IMPORTANT]
> 1. **Database:** Apakah ingin menggunakan **SQLite** (mudah, tidak perlu install server) atau **MySQL/PostgreSQL** (lebih profesional untuk TA)?
> 2. **Bahasa UI:** Apakah seluruh antarmuka dalam **Bahasa Indonesia** atau campuran Indonesia-Inggris?
> 3. **Logo PT Putra Hamid:** Apakah ada logo yang ingin digunakan, atau saya generate logo placeholder?

---

## Proposed Changes

### 📁 Struktur Folder Proyek

```
e:/Project/Website-Prediksi-Harga-Motor/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # SQLAlchemy models
│   ├── auth/
│   │   ├── routes.py        # Login/logout routes
│   │   └── forms.py
│   ├── dashboard/
│   │   └── routes.py
│   ├── users/
│   │   └── routes.py        # CRUD user
│   ├── dataset/
│   │   └── routes.py        # Import & preview dataset
│   ├── prediksi/
│   │   └── routes.py        # Training & prediksi
│   ├── evaluasi/
│   │   └── routes.py        # Evaluasi model
│   ├── ml/
│   │   ├── regression.py    # Core ML logic (sklearn)
│   │   ├── preprocessing.py # Label encoding, encoding
│   │   └── report.py        # PDF & Excel generator
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Design system (warna PT Putra Hamid)
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── charts.js    # Chart.js setup
│   │   │   └── datatables.js
│   │   └── uploads/         # Temp upload folder
│   └── templates/
│       ├── base.html         # Layout: sidebar + header + content
│       ├── auth/
│       │   └── login.html
│       ├── dashboard/
│       │   └── index.html
│       ├── users/
│       │   ├── index.html
│       │   └── form.html
│       ├── dataset/
│       │   ├── import.html
│       │   └── preview.html
│       ├── prediksi/
│       │   ├── training.html
│       │   ├── form.html
│       │   └── hasil.html
│       └── evaluasi/
│           └── index.html
├── config.py
├── run.py                   # Entry point Flask
├── requirements.txt
└── instance/
    └── database.db          # SQLite file (auto-generated)
```

---

### 🔐 Fase 1 — Auth & Dashboard

#### [NEW] `run.py`
Entry point aplikasi Flask.

#### [NEW] `config.py`
Konfigurasi: SECRET_KEY, DATABASE_URI, UPLOAD_FOLDER.

#### [NEW] `app/__init__.py`
Flask app factory dengan SQLAlchemy, LoginManager.

#### [NEW] `app/models.py`
SQLAlchemy models: `User`, `Dataset`, `MotorData`, `ModelTraining`, `PrediksiHasil`.

#### [NEW] `app/auth/routes.py`
- `GET/POST /login` — Form login + autentikasi session
- `GET /logout` — Clear session

#### [NEW] `app/dashboard/routes.py`
- `GET /dashboard` — Stats cards + chart data API

#### [NEW] `app/templates/base.html`
Layout utama: sidebar navigasi, topbar (nama admin + logout), content area.

#### [NEW] `app/templates/auth/login.html`
Form login dengan logo PT Putra Hamid.

#### [NEW] `app/templates/dashboard/index.html`
Cards statistik + 3 chart (Histogram harga, Line aktual vs prediksi, Bar/Pie merek).

---

### 👥 Fase 2 — Kelola User

#### [NEW] `app/users/routes.py`
- `GET /users` — Daftar user (DataTables)
- `GET/POST /users/tambah` — Form tambah user
- `GET/POST /users/edit/<id>` — Form edit user
- `POST /users/hapus/<id>` — Hapus user (dengan konfirmasi modal)

---

### 📂 Fase 3 — Import Dataset

#### [NEW] `app/dataset/routes.py`
- `GET/POST /dataset/import` — Upload CSV/Excel (drag & drop)
- `GET /dataset/preview/<id>` — Preview 10 baris + validasi
- `GET /dataset/riwayat` — Riwayat import
- `GET /dataset/report/<id>` — Generate PDF/Excel statistik dataset

#### [NEW] `app/ml/preprocessing.py`
- Label encoding variabel kategorikal
- Validasi kolom dataset
- Statistik deskriptif

---

### 🔮 Fase 4 — Prediksi (Core Feature)

#### [NEW] `app/prediksi/routes.py`
- `GET/POST /prediksi/training` — Pilih dataset, rasio split, jalankan training
- `GET/POST /prediksi/form` — Form input 8 variabel → hasil prediksi harga
- `GET /prediksi/hasil` — Riwayat prediksi (DataTables + filter)
- `GET /prediksi/report/<id>` — PDF/Excel report hasil prediksi
- `GET /prediksi/report-koefisien/<model_id>` — PDF report koefisien regresi

#### [NEW] `app/ml/regression.py`
- `train_model(dataset_id, rasio_train)` — Training dengan sklearn LinearRegression
- `predict_single(model_id, input_data)` — Prediksi 1 motor
- Simpan koefisien ke database (JSON)

---

### 📊 Fase 5 — Evaluasi Model

#### [NEW] `app/evaluasi/routes.py`
- `GET /evaluasi` — Tampilkan metrik (R², MAE, RMSE, MAPE) + grafik
- `GET /evaluasi/report/<model_id>` — PDF/Excel report evaluasi

---

### 📄 Report System

#### [NEW] `app/ml/report.py`
- `generate_pdf_dataset_report(dataset_id)` — Statistik dataset → PDF
- `generate_pdf_prediksi_report(prediksi_id)` — Hasil prediksi → PDF
- `generate_pdf_koefisien_report(model_id)` — Koefisien regresi → PDF
- `generate_pdf_evaluasi_report(model_id)` — Evaluasi model → PDF
- Versi Excel untuk semua report di atas

---

### 🎨 Design System

#### [NEW] `app/static/css/style.css`
Implementasi design system PT Putra Hamid:
- Primary: `#1E3A5F` (Biru Korporat)
- Secondary: `#2E86C1` (Biru Muda)
- Accent: `#E67E22` (Oranye)
- Layout: Sidebar fixed kiri + topbar + main content
- Glassmorphism cards, smooth hover animations

---

## Verification Plan

### Automated Tests
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Jalankan server
python run.py

# 3. Akses di browser
# http://localhost:5000
```

### Manual Verification
1. Login dengan akun default (admin/admin123)
2. Upload sample dataset CSV motor bekas
3. Jalankan training model
4. Input prediksi motor baru → cek hasil harga
5. Lihat evaluasi model (R², MAE, RMSE, MAPE)
6. Export report PDF

### Sample Dataset
Saya akan menyertakan **sample dataset CSV** berisi ~100 data motor bekas untuk testing.
