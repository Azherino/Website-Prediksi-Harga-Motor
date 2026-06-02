from app import create_app, db
from app.models import User
import bcrypt, os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Seed default superadmin
        if not User.query.filter_by(username='admin').first():
            hashed = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')
            admin = User(
                nama='Administrator',
                username='admin',
                email='admin@putrahamid.com',
                password=hashed,
                role='superadmin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created  ->  username: admin | password: admin123")
    app.run(debug=True, host='0.0.0.0', port=5000)
