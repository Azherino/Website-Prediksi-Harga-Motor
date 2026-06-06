from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.users import users_bp
from app.models import User
from app import db
import bcrypt


def superadmin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'superadmin':
            flash('Hanya Super Admin yang dapat mengakses halaman ini.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated


@users_bp.route('/')
@login_required
def index():
    search = request.args.get('q', '').strip()
    query  = User.query
    if search:
        query = query.filter(
            (User.nama.ilike(f'%{search}%')) |
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    page  = request.args.get('page', 1, type=int)
    users = query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('users/index.html', users=users, search=search)


@users_bp.route('/tambah', methods=['GET', 'POST'])
@login_required
@superadmin_required
def tambah():
    if request.method == 'POST':
        nama       = request.form.get('nama', '').strip()
        username   = request.form.get('username', '').strip()
        email      = request.form.get('email', '').strip()
        password   = request.form.get('password', '').strip()
        konfirmasi = request.form.get('konfirmasi_password', '').strip()
        role       = request.form.get('role', 'admin')

        errors = []
        if not all([nama, username, email, password]):
            errors.append('Semua field wajib diisi.')
        if password != konfirmasi:
            errors.append('Password dan konfirmasi tidak cocok.')
        if User.query.filter_by(username=username).first():
            errors.append('Username sudah digunakan.')
        if User.query.filter_by(email=email).first():
            errors.append('Email sudah digunakan.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('users/form.html', mode='tambah',
                                   form_data=request.form)

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user   = User(nama=nama, username=username, email=email,
                      password=hashed, role=role)
        db.session.add(user)
        db.session.commit()
        flash('User berhasil ditambahkan.', 'success')
        return redirect(url_for('users.index'))

    return render_template('users/form.html', mode='tambah', form_data={})


@users_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    if current_user.role != 'superadmin' and current_user.id != user_id:
        flash('Anda tidak memiliki akses untuk mengedit pengguna ini.', 'danger')
        return redirect(url_for('users.index'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.nama  = request.form.get('nama', user.nama).strip()
        user.email = request.form.get('email', user.email).strip()
        
        if current_user.role == 'superadmin':
            user.role  = request.form.get('role', user.role)

        new_pass = request.form.get('password', '').strip()
        if new_pass:
            konfirmasi = request.form.get('konfirmasi_password', '').strip()
            if new_pass != konfirmasi:
                flash('Password dan konfirmasi tidak cocok.', 'danger')
                return render_template('users/form.html', mode='edit', user=user,
                                       form_data=request.form)
            user.password = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()

        db.session.commit()
        flash('Data user berhasil diperbarui.', 'success')
        return redirect(url_for('users.index'))

    return render_template('users/form.html', mode='edit', user=user, form_data={})


@users_bp.route('/hapus/<int:user_id>', methods=['POST'])
@login_required
@superadmin_required
def hapus(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Anda tidak dapat menghapus akun sendiri.', 'danger')
        return redirect(url_for('users.index'))
    db.session.delete(user)
    db.session.commit()
    flash('User berhasil dihapus.', 'success')
    return redirect(url_for('users.index'))
