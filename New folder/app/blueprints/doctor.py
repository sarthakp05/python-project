from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.decorators import role_required
from app.models import Doctor, Appointment, Prescription, db
from app.forms import PrescriptionForm
from datetime import date

doctor_bp = Blueprint('doctor_bp', __name__)

@doctor_bp.route('/dashboard')
@login_required
@role_required(['doctor'])
def dashboard():
    doctor = current_user.doctor_profile
    if not doctor:
        flash("Doctor profile not found.", "danger")
        return redirect(url_for('auth_bp.login'))

    todays_appointments = Appointment.query.filter_by(
        doctor_id=doctor.id, appointment_date=date.today()
    ).all()
    
    recent_prescriptions = Prescription.query.join(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).order_by(Prescription.created_at.desc()).limit(5).all()

    return render_template('doctor/dashboard.html', 
                            doctor=doctor,
                            appointments=todays_appointments,
                            prescriptions=recent_prescriptions)

@doctor_bp.route('/appointment/<int:id>/prescribe', methods=['GET', 'POST'])
@login_required
@role_required(['doctor'])
def prescribe(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.doctor_id != current_user.doctor_profile.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('doctor_bp.dashboard'))
        
    form = PrescriptionForm()
    if form.validate_on_submit():
        prescription = Prescription(
            appointment_id=appointment.id,
            diagnosis=form.diagnosis.data,
            medicines=form.medicines.data, # using JSON string directly for simplicity
            instructions=form.instructions.data,
            follow_up_date=form.follow_up_date.data
        )
        appointment.status = 'completed'
        db.session.add(prescription)
        db.session.commit()
        flash("Prescription saved successfully.", "success")
        return redirect(url_for('doctor_bp.dashboard'))
        
    return render_template('doctor/prescribe.html', form=form, appointment=appointment)
