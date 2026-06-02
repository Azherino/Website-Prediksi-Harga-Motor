from app import create_app, db
from app.models import ModelTraining, PrediksiHasil

app = create_app()

with app.app_context():
    # Find all orphaned ModelTraining records
    orphaned_models = ModelTraining.query.filter_by(dataset_id=None).all()
    model_ids = [m.id for m in orphaned_models]
    
    if model_ids:
        print(f"Found {len(model_ids)} orphaned models. Deleting...")
        
        # Delete related PrediksiHasil first to avoid FK issues if cascade isn't fully active yet
        deleted_prediksi = PrediksiHasil.query.filter(PrediksiHasil.model_id.in_(model_ids)).delete(synchronize_session=False)
        print(f"Deleted {deleted_prediksi} related prediction records.")
        
        # Delete the models
        deleted_models = ModelTraining.query.filter(ModelTraining.id.in_(model_ids)).delete(synchronize_session=False)
        print(f"Deleted {deleted_models} orphaned model records.")
        
        db.session.commit()
    else:
        print("No orphaned models found.")
        
    # Also clean up any orphaned PrediksiHasil directly just in case
    orphaned_prediksi = PrediksiHasil.query.filter_by(model_id=None).delete(synchronize_session=False)
    if orphaned_prediksi:
        print(f"Deleted {orphaned_prediksi} orphaned prediction records.")
        db.session.commit()

print("Cleanup complete.")
