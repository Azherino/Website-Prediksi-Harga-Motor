# 📋 Planning Website — Prediksi Harga Motor Bekas
### Tugas Akhir: "Implementasi Metode Data Mining Dalam Prediksi Harga Motor Bekas Di PT Putra Hamid Dengan Regresi Linear Berganda"

---

## 1. 🎯 Overview Proyek

| Atribut | Detail |
|---|---|
| **Nama Sistem** | Sistem Prediksi Harga Motor Bekas PT Putra Hamid |
| **Metode** | Data Mining — Regresi Linear Berganda |
| **Target User** | Admin PT Putra Hamid |
| **Platform** | Web Application |
| **Tujuan** | Memprediksi harga motor bekas berdasarkan 8 variabel input |

---

## 2. 👤 Aktor & Hak Akses

Berdasarkan Use Case Diagram, sistem hanya memiliki **1 aktor**:

| Aktor | Deskripsi | Akses |
|---|---|---|
| **Admin** | Pengguna internal PT Putra Hamid | Full access ke semua fitur setelah login |

> ⚠️ Semua fitur **wajib login** terlebih dahulu (relasi `<<include>>` ke Login pada use case diagram).

---

## 3. 📦 Variabel Prediktor (Fitur Input)

Delapan variabel yang digunakan sebagai input model Regresi Linear Berganda:

| No | Variabel | Tipe Data | Keterangan |
|---|---|---|---|
| 1 | **Tahun Produksi** | Numerik (Integer) | Contoh: 2015, 2019, 2022 |
| 2 | **Kapasitas Mesin** | Numerik (Float) | Satuan cc, contoh: 110, 125, 150 |
| 3 | **Jarak Tempuh** | Numerik (Float) | Satuan km, contoh: 15000, 30000 |
| 4 | **Merek Motor** | Kategorikal | Contoh: Honda, Yamaha, Suzuki, Kawasaki |
| 5 | **Kondisi Fisik Motor** | Ordinal | Skala: Buruk / Cukup / Baik / Sangat Baik |
| 6 | **Tipe/Model Motor** | Kategorikal | Contoh: Matic, Manual, Sport |
| 7 | **Kelengkapan Surat-Surat** | Kategorikal | Contoh: Lengkap / Tidak Lengkap / BPKB Saja |
| 8 | **Pajak** | Biner | Aktif / Mati |

> 💡 Variabel kategorikal dan ordinal akan di-encode sebelum diproses model (Label Encoding / One-Hot Encoding). Variabel **Pajak** di-encode sebagai biner: `Aktif = 1`, `Mati = 0`.

---

## 4. 🗺️ Peta Fitur & Halaman

```
SISTEM PREDIKSI HARGA MOTOR BEKAS
│
├── 🔐 LOGIN
│
├── 🏠 DASHBOARD
│
├── 👥 KELOLA USER
│   ├── Daftar User
│   ├── Tambah User
│   ├── Edit User
│   └── Hapus User
│
├── 📂 IMPORT DATASET
│   ├── Upload File (.csv / .xlsx)
│   ├── Preview Data
│   ├── Validasi Data
│   └── 📄 Report Statistik Dataset
│
├── 🔮 PREDIKSI
│   ├── Proses Prediksi (Training Model)
│   ├── Form Input Prediksi Baru
│   ├── Lihat Hasil Prediksi
│   ├── 📄 Report Hasil Prediksi
│   └── 📄 Report Koefisien Regresi
│
└── 📊 EVALUASI MODEL
    ├── Proses Evaluasi
    ├── Lihat Evaluasi Model
    └── 📄 Report Evaluasi Model
```

---

## 5. 📄 Detail Setiap Halaman

### 5.1 🔐 Halaman Login
- **Fungsi:** Autentikasi admin sebelum mengakses sistem
- **Komponen UI:**
  - Logo / Nama Perusahaan PT Putra Hamid
  - Input: Username / Email
  - Input: Password (dengan toggle show/hide)
  - Tombol: Login
  - Pesan error jika kredensial salah
- **Validasi:** Field tidak boleh kosong, cek kredensial ke database
- **Redirect:** Jika berhasil → Dashboard

---

### 5.2 🏠 Halaman Dashboard
- **Fungsi:** Ringkasan dan overview sistem secara keseluruhan
- **Komponen UI:**
  - Sidebar navigasi (Login, Dashboard, Kelola User, Import Dataset, Prediksi, Evaluasi Model)
  - Header dengan nama admin & tombol logout
  - **Cards Statistik:**
    - Total Data Motor di Dataset
    - Jumlah Prediksi yang Telah Dilakukan
    - Akurasi Model Terakhir (R² Score)
    - Rata-rata Harga Prediksi
  - **Grafik / Chart:**
    - Distribusi Harga Motor (Histogram)
    - Perbandingan Harga Aktual vs Prediksi (Line Chart)
    - Distribusi per Merek Motor (Bar/Pie Chart)
  - Tabel ringkasan prediksi terbaru (5 data terakhir)

---

### 5.3 👥 Halaman Kelola User
> Relasi: `Admin → Kelola User` (use case diagram)

- **Fungsi:** Manajemen akun admin yang dapat mengakses sistem
- **Sub-halaman:**

#### 5.3.1 Daftar User
  - Tabel: No | Nama | Username | Email | Role | Aksi
  - Tombol: Tambah User
  - Fitur: Search, Filter, Pagination

#### 5.3.2 Form Tambah / Edit User
  - Input: Nama Lengkap
  - Input: Username
  - Input: Email
  - Input: Password (+ Konfirmasi Password)
  - Select: Role (Admin / Super Admin)
  - Tombol: Simpan / Batal

#### 5.3.3 Hapus User
  - Modal konfirmasi sebelum menghapus

---

### 5.4 📂 Halaman Import Dataset
> Relasi: `Admin → Import Dataset <<include>> Login` (use case diagram)

- **Fungsi:** Upload dan kelola dataset motor bekas untuk training model
- **Komponen UI:**

#### 5.4.1 Form Upload Dataset
  - Drag & Drop / Browse file (.csv atau .xlsx)
  - Informasi format file yang diterima
  - Tombol: Upload & Proses
  - Progress bar saat upload

#### 5.4.2 Preview & Validasi Data
  - Tabel preview 10 baris pertama data
  - Informasi: Jumlah baris, jumlah kolom, kolom yang terdeteksi
  - Validasi: Cek missing values, tipe data, kolom yang dibutuhkan
  - Indikator: ✅ Valid / ⚠️ Ada Missing Value / ❌ Format Salah

#### 5.4.3 Riwayat Import Dataset
  - Tabel: No | Nama File | Tanggal Upload | Jumlah Data | Status | Aksi

---

### 📄 Report Statistik Dataset
- **Trigger:** Setelah dataset berhasil diimport
- **Isi Report:**

| Informasi | Detail |
|---|---|
| Jumlah Total Data | N baris |
| Jumlah Kolom | 9 (8 variabel + 1 target) |
| Missing Values | Per kolom |
| **Statistik Deskriptif Numerik** | Min, Max, Mean, Median, Std Dev untuk: Tahun Produksi, Kapasitas Mesin, Jarak Tempuh, Harga |
| **Distribusi Kategorikal** | Frekuensi per kategori: Merek, Tipe, Kondisi, Kelengkapan Surat, Pajak (Aktif/Mati) |
| Visualisasi | Histogram distribusi harga, Box plot per variabel |

- **Format Export:** PDF / Excel

---

### 5.5 🔮 Halaman Prediksi
> Relasi: `Admin → Proses Prediksi <<extend>> Lihat Hasil Prediksi <<include>> Login`

- **Sub-halaman:**

#### 5.5.1 Proses Prediksi (Training Model)
- **Fungsi:** Melatih model Regresi Linear Berganda menggunakan dataset yang telah diimport
- **Komponen UI:**
  - Pilih dataset yang akan digunakan (dropdown riwayat import)
  - Konfigurasi split data: Slider rasio Train/Test (default: 80%/20%)
  - Pilihan preprocessing: Normalisasi / Standardisasi (opsional)
  - Tombol: **Proses Training**
  - Loading indicator saat model sedang dilatih
  - Notifikasi sukses / gagal

#### 5.5.2 Form Input Prediksi Baru (Single Prediction)
- **Fungsi:** Memprediksi harga 1 motor berdasarkan input manual admin
- **Form Fields:**

| Field | Tipe Input | Contoh |
|---|---|---|
| Tahun Produksi | Number Input | 2020 |
| Kapasitas Mesin (cc) | Number Input | 125 |
| Jarak Tempuh (km) | Number Input | 25000 |
| Merek Motor | Dropdown | Honda / Yamaha / Suzuki / dll |
| Kondisi Fisik | Radio / Select | Buruk / Cukup / Baik / Sangat Baik |
| Tipe/Model Motor | Dropdown | Matic / Manual / Sport |
| Kelengkapan Surat | Select | Lengkap / Tidak Lengkap / BPKB Saja |
| Pajak | Radio Button | 🟢 Aktif / 🔴 Mati |

- **Output:** Hasil prediksi harga dalam format **Rp xxx.xxx.xxx**
- Tombol: **Prediksi** dan **Reset**

#### 5.5.3 Lihat Hasil Prediksi
- **Fungsi:** Menampilkan riwayat semua hasil prediksi
- **Komponen UI:**
  - Tabel: No | Tahun | CC | KM | Merek | Kondisi | Tipe | Surat | Pajak | Harga Prediksi | Tanggal | Aksi
  - Filter by: Merek, Tipe, Tanggal
  - Search bar
  - Pagination
  - Tombol Export per baris / bulk export

---

### 📄 Report Hasil Prediksi
- **Trigger:** Dari halaman Lihat Hasil Prediksi
- **Isi Report:**

| Informasi | Detail |
|---|---|
| Identitas | Nama admin, tanggal cetak, nama PT |
| Detail Input | 8 variabel yang diinputkan (termasuk Pajak) |
| Hasil Prediksi | Harga dalam Rupiah |
| Perbandingan | Jika ada data aktual: Harga Aktual vs Prediksi, selisih (error) |
| Visualisasi | Scatter plot Aktual vs Prediksi (jika batch) |

- **Format Export:** PDF / Excel

---

### 📄 Report Koefisien Regresi
- **Trigger:** Setelah model selesai dilatih
- **Isi Report:**

| Informasi | Detail |
|---|---|
| Persamaan Regresi | Ŷ = β₀ + β₁X₁ + β₂X₂ + ... + β₈X₈ |
| Tabel Koefisien | Variabel, Koefisien (β), Std Error, t-value, p-value |
| Interpretasi | Pengaruh positif/negatif tiap variabel terhadap harga |
| Signifikansi | Variabel yang signifikan (p < 0.05) diberi tanda ✅ |

- **Format Export:** PDF / Excel

---

### 5.6 📊 Halaman Evaluasi Model
> Relasi: `Admin → Proses Evaluasi <<extend>> Lihat Evaluasi Model <<include>> Login`

#### 5.6.1 Proses Evaluasi
- **Fungsi:** Menjalankan evaluasi performa model menggunakan data test
- **Trigger:** Setelah Training Model selesai
- **Output Metrik yang Dihitung:**

| Metrik | Rumus / Keterangan |
|---|---|
| **R² (R-Squared)** | Koefisien determinasi, seberapa baik model menjelaskan variasi data |
| **MAE** | Mean Absolute Error |
| **RMSE** | Root Mean Squared Error |
| **MAPE** | Mean Absolute Percentage Error |

#### 5.6.2 Lihat Evaluasi Model
- **Komponen UI:**
  - Cards metrik evaluasi (R², MAE, RMSE, MAPE) dengan indikator warna (hijau = baik, kuning = cukup, merah = buruk)
  - Grafik: Scatter Plot Harga Aktual vs Harga Prediksi
  - Grafik: Residual Plot (Error Distribution)
  - Grafik: Learning Curve (opsional)
  - Riwayat evaluasi model sebelumnya (perbandingan antar training)

---

### 📄 Report Evaluasi Model
- **Trigger:** Dari halaman Lihat Evaluasi Model
- **Isi Report:**

| Informasi | Detail |
|---|---|
| Identitas Model | Tanggal training, dataset yang digunakan, rasio split |
| Metrik Evaluasi | R², MAE, MSE, RMSE, MAPE |
| Interpretasi | Kesimpulan performa model dalam bahasa Indonesia |
| Tabel Perbandingan | Harga Aktual vs Harga Prediksi (data test) |
| Visualisasi | Scatter plot, residual plot |

- **Format Export:** PDF / Excel

---

## 6. 🔗 Relasi Antar Fitur (Berdasarkan Use Case Diagram)

```
LOGIN
  ├── <<include>> dari: Kelola User
  ├── <<include>> dari: Import Dataset
  ├── <<include>> dari: Lihat Hasil Prediksi
  └── <<include>> dari: Lihat Evaluasi Model

LIHAT HASIL PREDIKSI
  └── <<extend>> oleh: Proses Prediksi
      (Prediksi baru akan memperluas tampilan hasil)

LIHAT EVALUASI MODEL
  └── <<extend>> oleh: Proses Evaluasi
      (Evaluasi baru akan memperluas tampilan evaluasi)
```

---

## 7. 🗄️ Struktur Database (Rancangan Awal)

### Tabel: `users`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT (PK) | Auto increment |
| nama | VARCHAR | Nama lengkap |
| username | VARCHAR | Unique |
| email | VARCHAR | Unique |
| password | VARCHAR | Hash (bcrypt) |
| role | ENUM | admin / superadmin |
| created_at | TIMESTAMP | |

### Tabel: `datasets`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT (PK) | |
| nama_file | VARCHAR | Nama file asli |
| path_file | VARCHAR | Path penyimpanan |
| jumlah_data | INT | |
| status | ENUM | valid / invalid |
| uploaded_by | INT (FK) | → users.id |
| created_at | TIMESTAMP | |

### Tabel: `motor_data`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT (PK) | |
| dataset_id | INT (FK) | → datasets.id |
| tahun_produksi | INT | |
| kapasitas_mesin | FLOAT | cc |
| jarak_tempuh | FLOAT | km |
| merek_motor | VARCHAR | |
| kondisi_fisik | ENUM | Buruk/Cukup/Baik/Sangat Baik |
| tipe_motor | VARCHAR | |
| kelengkapan_surat | VARCHAR | |
| pajak | ENUM | Aktif / Mati |
| harga_aktual | BIGINT | Rupiah |

### Tabel: `model_training`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT (PK) | |
| dataset_id | INT (FK) | |
| rasio_train | FLOAT | Contoh: 0.8 |
| koefisien | JSON | Array koefisien β |
| intercept | FLOAT | β₀ |
| r2_score | FLOAT | |
| mae | FLOAT | |
| mse | FLOAT | |
| rmse | FLOAT | |
| mape | FLOAT | |
| trained_by | INT (FK) | → users.id |
| created_at | TIMESTAMP | |

### Tabel: `prediksi_hasil`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INT (PK) | |
| model_id | INT (FK) | → model_training.id |
| tahun_produksi | INT | |
| kapasitas_mesin | FLOAT | |
| jarak_tempuh | FLOAT | |
| merek_motor | VARCHAR | |
| kondisi_fisik | VARCHAR | |
| tipe_motor | VARCHAR | |
| kelengkapan_surat | VARCHAR | |
| pajak | ENUM | Aktif / Mati |
| harga_prediksi | BIGINT | |
| harga_aktual | BIGINT | Nullable |
| predicted_by | INT (FK) | → users.id |
| created_at | TIMESTAMP | |

---

## 8. 🛠️ Rekomendasi Tech Stack

### Frontend
| Teknologi | Keterangan |
|---|---|
| **HTML / CSS / JavaScript** | atau framework seperti **React.js / Vue.js** |
| **Bootstrap 5** / **Tailwind CSS** | Framework CSS untuk UI |
| **Chart.js** / **ApexCharts** | Library visualisasi grafik |
| **DataTables.js** | Tabel interaktif dengan search & pagination |

### Backend
| Teknologi | Keterangan |
|---|---|
| **Python (Flask / FastAPI)** | ✅ Direkomendasikan karena integrasi mudah dengan scikit-learn |
| atau **PHP (Laravel)** | Jika tidak menggunakan Python |

### Machine Learning
| Teknologi | Keterangan |
|---|---|
| **scikit-learn** | `LinearRegression` untuk model regresi |
| **pandas** | Manipulasi dataset |
| **numpy** | Komputasi numerik |
| **matplotlib / seaborn** | Visualisasi grafik untuk report |

### Database
| Teknologi | Keterangan |
|---|---|
| **MySQL** / **PostgreSQL** | Database relasional |

### Export Report
| Teknologi | Keterangan |
|---|---|
| **ReportLab / WeasyPrint** (Python) | Generate PDF |
| **openpyxl / xlsxwriter** (Python) | Generate Excel |

---

## 9. 🎨 Design System (Panduan UI)

### Palet Warna
| Elemen | Warna | Hex |
|---|---|---|
| Primary | Biru Korporat | `#1E3A5F` |
| Secondary | Biru Muda | `#2E86C1` |
| Accent | Oranye | `#E67E22` |
| Success | Hijau | `#27AE60` |
| Warning | Kuning | `#F39C12` |
| Danger | Merah | `#E74C3C` |
| Background | Abu Terang | `#F5F6FA` |
| Text | Abu Gelap | `#2C3E50` |

### Layout Utama
```
┌─────────────────────────────────────────────┐
│              HEADER / TOPBAR                │
├──────────┬──────────────────────────────────┤
│          │                                  │
│ SIDEBAR  │         MAIN CONTENT             │
│          │                                  │
│ - Dashboard      ┌──────────────────────┐   │
│ - Kelola User    │   Cards / Tables /   │   │
│ - Import Dataset │   Charts / Forms     │   │
│ - Prediksi       └──────────────────────┘   │
│ - Evaluasi Model                            │
│          │                                  │
└──────────┴──────────────────────────────────┘
```

---

## 10. 📐 Alur Kerja Sistem (Flow Lengkap)

```
1. Admin buka web → Halaman LOGIN
          ↓
2. Masukkan username & password → Autentikasi
          ↓
3. Berhasil login → DASHBOARD
          ↓
4. IMPORT DATASET → Upload file CSV/Excel
          ↓ (jika berhasil)
5. Preview & Validasi Data → Simpan ke database
          ↓ (opsional)
   Generate REPORT STATISTIK DATASET
          ↓
6. PREDIKSI → Proses Training Model (pilih dataset)
          ↓
   Generate REPORT KOEFISIEN REGRESI
          ↓
7. EVALUASI MODEL → Proses Evaluasi (otomatis dari training)
          ↓
   Generate REPORT EVALUASI MODEL
          ↓
8. Input motor baru → Form Prediksi → Hasil Prediksi
          ↓
   Generate REPORT HASIL PREDIKSI
```

---

## 11. ✅ Checklist Pengembangan

### Fase 1 — Setup & Autentikasi
- [ ] Setup project (folder structure, environment)
- [ ] Konfigurasi database
- [ ] Halaman Login + Autentikasi (session/JWT)
- [ ] Middleware proteksi route (wajib login)
- [ ] Halaman Dashboard (layout dasar)

### Fase 2 — Kelola User
- [ ] CRUD User (Create, Read, Update, Delete)
- [ ] Validasi form input
- [ ] Search & Pagination tabel user

### Fase 3 — Import Dataset
- [ ] Form upload file CSV/Excel
- [ ] Parsing & validasi file
- [ ] Preview data dalam tabel
- [ ] Simpan data ke database
- [ ] Report Statistik Dataset (generate PDF/Excel)

### Fase 4 — Prediksi (Core Feature)
- [ ] Implementasi model Regresi Linear Berganda
- [ ] Preprocessing data (encoding kategorikal, normalisasi)
- [ ] Training model + simpan koefisien
- [ ] Form prediksi single input
- [ ] Simpan & tampilkan riwayat prediksi
- [ ] Report Hasil Prediksi (generate PDF/Excel)
- [ ] Report Koefisien Regresi (generate PDF/Excel)

### Fase 5 — Evaluasi Model
- [ ] Kalkulasi metrik (R², MAE, MSE, RMSE, MAPE)
- [ ] Tampilkan grafik evaluasi (scatter plot, residual plot)
- [ ] Riwayat evaluasi antar model
- [ ] Report Evaluasi Model (generate PDF/Excel)

### Fase 6 — Finalisasi
- [ ] Integrasi chart di Dashboard
- [ ] Responsive design (mobile-friendly)
- [ ] Testing & bug fixing
- [ ] Dokumentasi (untuk laporan TA)

---

*Dokumen ini merupakan planning awal pengembangan website Tugas Akhir.*
*Dapat direvisi sesuai kebutuhan dan masukan dari dosen pembimbing.*