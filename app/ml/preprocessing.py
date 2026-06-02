import pandas as pd
import numpy as np

# ── Ordinal & Binary encoding maps ─────────────────────────────────────────
# Updated to match dataset: Buruk=1, Cukup=2, Baik=3
KONDISI_MAP = {'Buruk': 1, 'Cukup': 2, 'Baik': 3}
PAJAK_MAP   = {'Mati': 0,  'Hidup': 1}
SURAT_MAP   = {'Tidak Lengkap': 0, 'Lengkap': 1}

REQUIRED_COLUMNS = [
    'tahun_produksi', 'kapasitas_mesin', 'jarak_tempuh',
    'merek_motor', 'kondisi_fisik', 'tipe_motor',
    'model_motor', 'kelengkapan_surat', 'pajak', 'harga_aktual'
]

# ── Mapping variasi nama kolom → nama standar ────────────────────────────────
COLUMN_ALIASES = {
    'tahun_produksi':    ['tahun produksi', 'tahun', 'year', 'thn produksi', 'tahun_produksi'],
    'kapasitas_mesin':   ['kapasitas mesin (cc)', 'kapasitas mesin', 'cc', 'mesin (cc)',
                          'kapasitas_mesin', 'kapasitas mesin(cc)', 'engine capacity'],
    'jarak_tempuh':      ['jarak tempuh (km)', 'jarak tempuh', 'km', 'odometer',
                          'jarak_tempuh', 'jarak tempuh(km)', 'kilometre'],
    'merek_motor':       ['merek motor', 'merek', 'brand', 'merk motor', 'merk',
                          'merek_motor'],
    'kondisi_fisik':     ['kondisi fisik motor', 'kondisi fisik', 'kondisi', 'condition',
                          'kondisi_fisik', 'kondisi motor'],
    'tipe_motor':        ['tipe motor', 'tipe', 'type', 'jenis motor', 'jenis',
                          'tipe_motor'],
    'model_motor':       ['model motor', 'model', 'model_motor', 'nama model',
                          'nama motor'],
    'kelengkapan_surat': ['kelengkapan surat-surat', 'kelengkapan surat', 'surat',
                          'dokumen', 'kelengkapan_surat', 'surat-surat', 'documents'],
    'pajak':             ['pajak', 'tax', 'status pajak', 'pajak kendaraan'],
    'harga_aktual':      ['harga (rp)', 'harga', 'price', 'harga aktual', 'harga_aktual',
                          'harga jual', 'harga (rupiah)', 'harga motor', 'harga(rp)',
                          'harga motor bekas (rp)', 'harga motor bekas',
                          'harga aktual (rp)'],
}


def normalize_columns(df):
    """
    Rename kolom DataFrame agar sesuai nama standar.
    Pencocokan dilakukan case-insensitive dan trim spasi.
    Mengembalikan DataFrame baru dengan kolom yang sudah dinormalisasi.
    """
    rename_map = {}
    lower_cols = {col.strip().lower(): col for col in df.columns}

    for standard, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias.strip().lower() in lower_cols:
                original_col = lower_cols[alias.strip().lower()]
                if original_col != standard:
                    rename_map[original_col] = standard
                break

    if rename_map:
        df = df.rename(columns=rename_map)
    return df


def validate_columns(df):
    """Return list of missing required columns."""
    return [c for c in REQUIRED_COLUMNS if c not in df.columns]


def preprocess_dataframe(df):
    """
    Full preprocessing for training.
    Uses One-Hot Encoding (drop_first=True) for nominal variables
    (merek_motor, tipe_motor, model_motor) and Label Encoding for
    ordinal/binary variables (kondisi_fisik, kelengkapan_surat, pajak).

    Returns (X: np.ndarray, y: np.ndarray, feature_names: list[str])
    """
    data = df[REQUIRED_COLUMNS].copy().dropna()

    # Label encoding for ordinal & binary variables
    data['kondisi_enc'] = data['kondisi_fisik'].map(KONDISI_MAP).fillna(2)
    data['pajak_enc']   = data['pajak'].map(PAJAK_MAP).fillna(0)
    data['surat_enc']   = data['kelengkapan_surat'].map(SURAT_MAP).fillna(0)

    # One-Hot Encoding with drop_first=True to avoid dummy variable trap
    merek_dummies = pd.get_dummies(data['merek_motor'], prefix='merek', drop_first=True)
    tipe_dummies  = pd.get_dummies(data['tipe_motor'],  prefix='tipe',  drop_first=True)
    model_dummies = pd.get_dummies(data['model_motor'], prefix='model', drop_first=True)

    X = pd.concat([
        data[['tahun_produksi', 'kapasitas_mesin', 'jarak_tempuh']],
        merek_dummies,
        tipe_dummies,
        model_dummies,
        data[['kondisi_enc', 'pajak_enc', 'surat_enc']],
    ], axis=1)

    y = data['harga_aktual'].astype(float)
    return X.values.astype(float), y.values, list(X.columns)


def preprocess_single(input_dict, feature_names):
    """
    Preprocess a single prediction input dict.
    Returns np.ndarray of shape (1, n_features).
    """
    row = {name: 0.0 for name in feature_names}

    row['tahun_produksi']  = float(input_dict.get('tahun_produksi', 0))
    row['kapasitas_mesin'] = float(input_dict.get('kapasitas_mesin', 0))
    row['jarak_tempuh']    = float(input_dict.get('jarak_tempuh', 0))
    row['kondisi_enc']     = float(KONDISI_MAP.get(input_dict.get('kondisi_fisik', 'Baik'), 2))
    row['pajak_enc']       = float(PAJAK_MAP.get(input_dict.get('pajak', 'Hidup'), 1))
    row['surat_enc']       = float(SURAT_MAP.get(input_dict.get('kelengkapan_surat', 'Lengkap'), 1))

    # One-Hot dummy encoding for merek, tipe, model
    for key, prefix in [('merek_motor', 'merek'), ('tipe_motor', 'tipe'), ('model_motor', 'model')]:
        col = f"{prefix}_{input_dict.get(key, '')}"
        if col in row:
            row[col] = 1.0

    return np.array([[row[f] for f in feature_names]])


def get_dataset_stats(df):
    """Return descriptive statistics for dashboard / report."""
    stats = {}
    num_cols = ['tahun_produksi', 'kapasitas_mesin', 'jarak_tempuh', 'harga_aktual']
    for col in num_cols:
        if col in df.columns:
            stats[col] = {
                'min':    float(df[col].min()),
                'max':    float(df[col].max()),
                'mean':   round(float(df[col].mean()), 2),
                'median': float(df[col].median()),
                'std':    round(float(df[col].std()), 2),
            }
    cat_cols = ['merek_motor', 'tipe_motor', 'model_motor', 'kondisi_fisik',
                'kelengkapan_surat', 'pajak']
    for col in cat_cols:
        if col in df.columns:
            stats[col] = {str(k): int(v) for k, v in df[col].value_counts().items()}
    return stats
