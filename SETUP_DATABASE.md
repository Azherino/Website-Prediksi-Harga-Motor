# Panduan Instalasi dan Setup Database (Localhost)

Aplikasi ini menggunakan **MySQL** sebagai database utama dan **Flask-SQLAlchemy** sebagai ORM. 
Kabar baiknya, Anda tidak perlu repot-repot mengimpor file `.sql` secara manual karena aplikasi ini sudah dilengkapi dengan sistem **Auto-Migrate** dan **Seeder** otomatis!

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di komputer (localhost) Anda:

## 1. Persiapan Database MySQL
1. Pastikan Anda sudah menginstal dan menyalakan MySQL Server (menggunakan **XAMPP**, **Laragon**, **WAMP**, atau MySQL native).
2. Buka antarmuka manajemen database Anda (contoh: **phpMyAdmin** di `http://localhost/phpmyadmin` atau aplikasi *DBeaver*, *HeidiSQL*, dsb).
3. Buat sebuah database kosong baru dengan nama:
   ```text
   prediksi_motor
   ```

## 2. Konfigurasi Kredensial Database (Jika Perlu)
Secara bawaan (*default*), aplikasi ini akan mencoba terhubung ke database dengan kredensial:
- **Host**: localhost
- **Username**: root
- **Password**: *(kosong)*
- **Database**: prediksi_motor

Jika konfigurasi MySQL di komputer Anda berbeda (misalnya memiliki *password*), silakan edit file `config.py` pada baris berikut:
```python
# Ubah bagian ini sesuai dengan pengaturan MySQL Anda
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mysql+pymysql://root:password_anda@localhost/prediksi_motor'
```
> *Format URI: `mysql+pymysql://<username>:<password>@<host>/<nama_database>`*

## 3. Instalasi Dependensi
Pastikan Anda sudah menginstal **Python** (versi 3.8 ke atas disarankan).
Buka terminal/CMD/PowerShell di dalam folder project ini, lalu jalankan perintah:
```bash
pip install -r requirements.txt
```

## 4. Menjalankan Aplikasi dan Auto-Migrate
Setelah database `prediksi_motor` berhasil dibuat dan dependensi terinstal, Anda hanya perlu menjalankan aplikasinya.

Di dalam terminal project, jalankan:
```bash
python run.py
```

**Apa yang terjadi saat `python run.py` dijalankan?**
1. Aplikasi akan mendeteksi apakah tabel-tabel sudah ada di dalam database.
2. Jika tabel belum ada, SQLAlchemy akan **membuat seluruh tabel secara otomatis** sesuai struktur kode di `app/models.py`.
3. Aplikasi akan **membuat satu akun Superadmin secara otomatis** (jika belum ada di database).

## 5. Login ke Dalam Sistem
Buka browser Anda dan akses aplikasi di:
```text
http://localhost:5000 atau http://127.0.0.1:5000
```
Gunakan kredensial default yang telah digenerate secara otomatis untuk masuk:
- **Username**: `admin`
- **Password**: `admin123`

---
> **Catatan Penting**: Jika di masa mendatang ada perubahan struktur tabel (*kolom baru*) yang mengharuskan migrasi manual, Anda dapat menggunakan script tambahan `python migrate_db.py` (jika tersedia). Namun untuk penginstalan dari awal (*fresh install*), cukup ikuti 5 langkah di atas.
