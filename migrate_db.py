"""
Database migration script - Part 2:
Add model_motor column to motor_data and prediksi_hasil tables
"""
import pymysql
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='prediksi_motor',
    charset='utf8mb4'
)

cursor = conn.cursor()

print("=" * 60)
print("ADD model_motor COLUMN")
print("=" * 60)

# Add model_motor column if not exists
print("\n[1/2] Menambah kolom model_motor ke motor_data...")
try:
    cursor.execute("""
        ALTER TABLE motor_data 
        ADD COLUMN model_motor VARCHAR(50) NULL AFTER tipe_motor
    """)
    print("      OK - Kolom model_motor ditambahkan ke motor_data")
except pymysql.err.OperationalError as e:
    if 'Duplicate column' in str(e):
        print("      SKIP - Kolom model_motor sudah ada di motor_data")
    else:
        raise

print("[2/2] Menambah kolom model_motor ke prediksi_hasil...")
try:
    cursor.execute("""
        ALTER TABLE prediksi_hasil 
        ADD COLUMN model_motor VARCHAR(50) NULL AFTER tipe_motor
    """)
    print("      OK - Kolom model_motor ditambahkan ke prediksi_hasil")
except pymysql.err.OperationalError as e:
    if 'Duplicate column' in str(e):
        print("      SKIP - Kolom model_motor sudah ada di prediksi_hasil")
    else:
        raise

conn.commit()

# Verify
print("\n" + "=" * 60)
print("VERIFIKASI STRUKTUR TABEL")
print("=" * 60)

print("\n--- motor_data columns ---")
cursor.execute("DESCRIBE motor_data")
for row in cursor.fetchall():
    print(f"  {row[0]:25s} {row[1]}")

print("\n--- prediksi_hasil columns ---")
cursor.execute("DESCRIBE prediksi_hasil")
for row in cursor.fetchall():
    print(f"  {row[0]:25s} {row[1]}")

# Count remaining data
cursor.execute("SELECT COUNT(*) FROM datasets")
ds_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM motor_data")
md_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM model_training")
mt_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM prediksi_hasil")
ph_count = cursor.fetchone()[0]

print(f"\n--- Data counts (should all be 0) ---")
print(f"  datasets:       {ds_count}")
print(f"  motor_data:     {md_count}")
print(f"  model_training: {mt_count}")
print(f"  prediksi_hasil: {ph_count}")

print("\nMigrasi database selesai!")

cursor.close()
conn.close()
