from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.decorators import role_required
from app.models import User, Patient, Doctor, Appointment, Billing, db

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard')
@login_required
@role_required(['admin'])
def dashboard():
    # Gather stats
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    from datetime import date
    todays_appointments = Appointment.query.filter_by(appointment_date=date.today()).count()
    revenue_summary = db.session.query(db.func.sum(Billing.total_amount)).filter(Billing.payment_status == 'paid').scalar() or 0.0
    
    recent_activities = ["Dr. Smith logged in", "John Doe booked an appointment", "New Patient Alice registered"]
    
    return render_template('admin/dashboard.html',
                           total_patients=total_patients,
                           total_doctors=total_doctors,
                           todays_appointments=todays_appointments,
                           revenue_summary=revenue_summary,
                           recent_activities=recent_activities)

@admin_bp.route('/users')
@login_required
@role_required(['admin'])
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
@role_required(['admin'])
def delete_user(id):
    if current_user.id == id:
        flash("You cannot delete yourself!", "danger")
        return redirect(url_for('admin_bp.manage_users'))
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('admin_bp.manage_users'))
