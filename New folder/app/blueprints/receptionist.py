from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.decorators import role_required
from app.models import Appointment, Patient
import datetime

receptionist_bp = Blueprint('receptionist_bp', __name__)

@receptionist_bp.route('/dashboard')
@login_required
@role_required(['receptionist'])
def dashboard():
    today = datetime.date.today()
    todays_appointments = Appointment.query.filter_by(appointment_date=today).all()
    total_patients_today = Patient.query.filter(Patient.created_at >= today).count()
    
    return render_template('receptionist/dashboard.html', 
                           appointments=todays_appointments,
                           new_patients_count=total_patients_today)
