from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm
from urllib.parse import urlparse

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_bp.dashboard'))
        elif current_user.role == 'doctor':
            return redirect(url_for('doctor_bp.dashboard'))
        else:
            return redirect(url_for('auth_bp.login')) # Fallback
            
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth_bp.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            if user.role == 'admin':
                next_page = url_for('admin_bp.dashboard')
            elif user.role == 'doctor':
                next_page = url_for('doctor_bp.dashboard')
            else:
                next_page = url_for('auth_bp.login')
                
        # update last login? Here or in a signal.
        return redirect(next_page)
        
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    from app.forms import ProfileForm
    from app.extensions import db
    
    form = ProfileForm()
    if form.validate_on_submit():
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user and existing_user.id != current_user.id:
            flash("Email already registered.", "danger")
            return redirect(url_for('auth_bp.profile'))
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
            
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('auth_bp.profile'))
        
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    return render_template('auth/profile.html', form=form)
