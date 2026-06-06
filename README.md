# Website Prediksi Harga Motor Bekas - PT Putra Hamid

Aplikasi berbasis web untuk memprediksi harga motor bekas menggunakan **Metode Data Mining — Regresi Linear Berganda (Multiple Linear Regression)**. Proyek ini dikembangkan dengan framework **Flask** (Python) dan database **MySQL** untuk membantu PT Putra Hamid menentukan harga motor bekas secara objektif dan akurat berdasarkan 8 variabel spesifikasi motor.

---

## Fitur Utama

Sistem ini didesain khusus untuk kebutuhan internal admin PT Putra Hamid dengan fitur lengkap sebagai berikut:

*   **Autentikasi Admin:** Sistem login terproteksi dengan role management (Admin dan Superadmin) menggunakan enkripsi password `bcrypt`.
*   **Dashboard Interaktif:** Menampilkan metrik statistik penting (total dataset, jumlah prediksi, akurasi $R^2$ model, rata-rata harga) dan grafik distribusi visual.
*   **Kelola User (CRUD):** Manajemen akun pengguna/admin yang diizinkan mengakses sistem.
*   **Import Dataset:** Upload data motor bekas dalam format `.xlsx` atau `.csv`, lengkap dengan preview data, validasi data otomatis, serta laporan statistik deskriptif.
*   **Prediksi Harga:**
    *   **Training Model:** Melatih model Regresi Linear Berganda langsung dari web dengan mengatur rasio data *Train/Test*.
    *   **Form Prediksi:** Memprediksi harga motor secara instan dengan memasukkan 8 variabel spesifikasi motor.
    *   **Riwayat Prediksi:** Menyimpan dan menampilkan seluruh hasil riwayat perhitungan prediksi.
*   **Evaluasi Model:** Menampilkan metrik performa model ($R^2$, MAE, RMSE, MAPE) beserta grafik *Scatter Plot* (Aktual vs Prediksi) dan *Residual Plot*.
*   **Laporan PDF/Excel:** Cetak laporan hasil prediksi, evaluasi model, koefisien regresi, dan statistik dataset secara dinamis.

---

##  Teknologi & Library

*   **Backend:** Python 3.x, Flask (Web Framework)
*   **Database & ORM:** MySQL, Flask-SQLAlchemy, PyMySQL
*   **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib
*   **Export Laporan:** ReportLab, OpenPyXL, XLRD
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Chart.js (Visualisasi grafik)

---

##  Struktur Variabel Input Prediksi

Model prediksi harga menggunakan 8 variabel penentu berikut:

1.  **Tahun Produksi** (Numerik - Tahun)
2.  **Kapasitas Mesin** (Numerik - CC)
3.  **Jarak Tempuh** (Numerik - KM)
4.  **Merek Motor** (Kategorikal - Honda, Yamaha, dll.)
5.  **Kondisi Fisik Motor** (Ordinal - Buruk, Cukup, Baik, Sangat Baik)
6.  **Tipe/Model Motor** (Kategorikal - Matic, Manual, Sport)
7.  **Kelengkapan Surat** (Kategorikal - Lengkap, BPKB Saja, Tidak Lengkap)
8.  **Pajak** (Biner - Aktif / Mati)

---

##  Panduan Instalasi & Menjalankan Aplikasi

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi ini di komputer lokal Anda (*localhost*):

### 1. Prasyarat
Pastikan Anda sudah menginstal:
*   **Python 3.8 ke atas**
*   **MySQL Server** (melalui XAMPP, Laragon, WAMP, atau MySQL native)

### 2. Persiapan Database
1.  Aktifkan MySQL Server Anda.
2.  Buat database kosong baru bernama `prediksi_motor` melalui phpMyAdmin (`http://localhost/phpmyadmin`) atau database manager lainnya:
    ```sql
    CREATE DATABASE prediksi_motor;
    ```

### 3. Konfigurasi Lingkungan (.env)
1.  Salin file `.env.example` dan ubah namanya menjadi `.env`:
    ```bash
    cp .env.example .env
    ```
2.  Sesuaikan kredensial koneksi database MySQL pada baris `DATABASE_URL` jika password database Anda tidak kosong:
    ```env
    DATABASE_URL=mysql+pymysql://username:password@localhost/prediksi_motor
    ```

### 4. Instalasi Dependensi
Buka terminal/CMD di dalam folder project ini, lalu jalankan perintah:
```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi
Jalankan skrip utama aplikasi dengan perintah:
```bash
python run.py
```
> **Info:** Sistem akan mendeteksi database kosong, membuat seluruh tabel yang diperlukan secara otomatis (*Auto-Migrate*), dan mengisi akun Admin default (*Seeding*).

---

##  Kredensial Login Default

Setelah aplikasi berjalan, buka browser dan akses `http://localhost:5000`. Gunakan akun berikut untuk masuk:
*   **Username:** `admin`
*   **Password:** `admin123`
