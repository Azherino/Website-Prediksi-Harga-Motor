import numpy as np
import joblib
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pandas as pd

from .preprocessing import preprocess_dataframe, preprocess_single


def train_model(motor_data_objs, rasio_train=0.8, model_save_path=None):
    """
    Train Linear Regression from list of MotorData ORM objects.
    Returns a result dict with coefficients, metrics, and test predictions.
    """
    records = [
        {
            'tahun_produksi':    d.tahun_produksi,
            'kapasitas_mesin':   d.kapasitas_mesin,
            'jarak_tempuh':      d.jarak_tempuh,
            'merek_motor':       d.merek_motor,
            'kondisi_fisik':     d.kondisi_fisik,
            'tipe_motor':        d.tipe_motor,
            'model_motor':       d.model_motor,
            'kelengkapan_surat': d.kelengkapan_surat,
            'pajak':             d.pajak,
            'harga_aktual':      d.harga_aktual,
        }
        for d in motor_data_objs
    ]
    df = pd.DataFrame(records)

    X, y, feature_names = preprocess_dataframe(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=round(1 - rasio_train, 2), random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    r2   = float(r2_score(y_test, y_pred))
    mae  = float(mean_absolute_error(y_test, y_pred))
    mse  = float(mean_squared_error(y_test, y_pred))
    rmse = float(np.sqrt(mse))

    mask = y_test != 0
    mape = float(np.mean(np.abs((y_test[mask] - y_pred[mask]) / y_test[mask])) * 100)

    if model_save_path:
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        joblib.dump({'model': model, 'feature_names': feature_names}, model_save_path)

    coefficients = {name: float(coef)
                    for name, coef in zip(feature_names, model.coef_)}

    return {
        'feature_names': feature_names,
        'coefficients':  coefficients,
        'intercept':     float(model.intercept_),
        'r2':            r2,
        'mae':           mae,
        'mse':           mse,
        'rmse':          rmse,
        'mape':          mape,
        'y_test':        [float(v) for v in y_test],
        'y_pred':        [float(v) for v in y_pred],
        'train_size':    len(X_train),
        'test_size':     len(X_test),
    }


def predict_single(model_path, input_dict):
    """
    Load saved model and predict price for one motorcycle.
    Returns predicted price (float).
    """
    payload = joblib.load(model_path)
    model         = payload['model']
    feature_names = payload['feature_names']

    X = preprocess_single(input_dict, feature_names)
    price = model.predict(X)[0]
    return max(0.0, float(price))
