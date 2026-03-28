from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.decorators import role_required
from app.models import Appointment, Patient, Doctor, db
from app.forms import AppointmentForm

appointment_bp = Blueprint('appointment_bp', __name__)

@appointment_bp.route('/', methods=['GET'])
@login_required
@role_required(['admin', 'doctor', 'receptionist'])
def list_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()
    return render_template('appointment/list.html', appointments=appointments)

@appointment_bp.route('/book', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'receptionist'])
def book_appointment():
    form = AppointmentForm()
    # Populate choices dynamically
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    form.doctor_id.choices = [(d.id, f"Dr. {d.user.username} ({d.specialization})") for d in Doctor.query.all()]
    
    if form.validate_on_submit():
        # Validate no duplicate for the same time slot
        existing = Appointment.query.filter_by(
            doctor_id=form.doctor_id.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data
        ).first()
        
        if existing:
            flash("Doctor already has an appointment at this time.", "danger")
            return redirect(url_for('appointment_bp.book_appointment'))

        appt = Appointment(
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            symptoms=form.symptoms.data,
            status='scheduled'
        )
        db.session.add(appt)
        db.session.commit()
        flash("Appointment booked successfully.", "success")
        return redirect(url_for('appointment_bp.list_appointments'))
        
    return render_template('appointment/form.html', form=form, title="Book Appointment")

@appointment_bp.route('/<int:id>/status/<string:status>')
@login_required
@role_required(['admin', 'receptionist', 'doctor'])
def update_status(id, status):
    if status not in ['scheduled', 'completed', 'cancelled', 'no-show']:
        flash("Invalid status", "danger")
        return redirect(url_for('appointment_bp.list_appointments'))
        
    appt = Appointment.query.get_or_404(id)
    appt.status = status
    db.session.commit()
    flash(f"Appointment status updated to {status}", "success")
    return redirect(url_for('appointment_bp.list_appointments'))
