from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id         = db.Column(db.Integer, primary_key=True)
    nama       = db.Column(db.String(100), nullable=False)
    username   = db.Column(db.String(50),  unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.Enum('admin', 'superadmin'), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Dataset(db.Model):
    __tablename__ = 'datasets'
    id          = db.Column(db.Integer, primary_key=True)
    nama_file   = db.Column(db.String(255), nullable=False)
    path_file   = db.Column(db.String(500), nullable=False)
    jumlah_data = db.Column(db.Integer, default=0)
    status      = db.Column(db.Enum('valid', 'invalid', 'pending'), default='pending')
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    uploader   = db.relationship('User',      backref='datasets')
    motor_data = db.relationship('MotorData', backref='dataset',
                                 lazy=True, cascade='all, delete-orphan')


class MotorData(db.Model):
    __tablename__ = 'motor_data'
    id                = db.Column(db.Integer, primary_key=True)
    dataset_id        = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=False)
    tahun_produksi    = db.Column(db.Integer,  nullable=False)
    kapasitas_mesin   = db.Column(db.Float,    nullable=False)
    jarak_tempuh      = db.Column(db.Float,    nullable=False)
    merek_motor       = db.Column(db.String(50),  nullable=False)
    kondisi_fisik     = db.Column(db.String(20),  nullable=False)
    tipe_motor        = db.Column(db.String(20),  nullable=False)
    model_motor       = db.Column(db.String(50),  nullable=True)
    kelengkapan_surat = db.Column(db.String(30),  nullable=False)
    pajak             = db.Column(db.String(10),  nullable=False)
    harga_aktual      = db.Column(db.BigInteger,  nullable=False)


class ModelTraining(db.Model):
    __tablename__ = 'model_training'
    id          = db.Column(db.Integer, primary_key=True)
    dataset_id  = db.Column(db.Integer, db.ForeignKey('datasets.id', ondelete='CASCADE'))
    rasio_train = db.Column(db.Float,   default=0.8)
    koefisien   = db.Column(db.JSON)
    intercept   = db.Column(db.Float)
    model_path  = db.Column(db.String(500))
    r2_score    = db.Column(db.Float)
    mae         = db.Column(db.Float)
    mse         = db.Column(db.Float)
    rmse        = db.Column(db.Float)
    mape        = db.Column(db.Float)
    train_size  = db.Column(db.Integer)
    test_size   = db.Column(db.Integer)
    y_test_data = db.Column(db.JSON)
    y_pred_data = db.Column(db.JSON)
    trained_by  = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    trainer  = db.relationship('User',    backref='trained_models')
    dataset  = db.relationship('Dataset', backref=db.backref('trainings', cascade='all, delete-orphan'))
    prediksi = db.relationship('PrediksiHasil', backref='model', cascade='all, delete-orphan', lazy=True)


class PrediksiHasil(db.Model):
    __tablename__ = 'prediksi_hasil'
    id                = db.Column(db.Integer, primary_key=True)
    model_id          = db.Column(db.Integer, db.ForeignKey('model_training.id', ondelete='CASCADE'))
    tahun_produksi    = db.Column(db.Integer)
    kapasitas_mesin   = db.Column(db.Float)
    jarak_tempuh      = db.Column(db.Float)
    merek_motor       = db.Column(db.String(50))
    kondisi_fisik     = db.Column(db.String(20))
    tipe_motor        = db.Column(db.String(20))
    model_motor       = db.Column(db.String(50))
    kelengkapan_surat = db.Column(db.String(30))
    pajak             = db.Column(db.String(10))
    harga_prediksi    = db.Column(db.BigInteger)
    harga_aktual      = db.Column(db.BigInteger, nullable=True)
    predicted_by      = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)

    predictor = db.relationship('User', backref='predictions')
