from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import Doctor, Patient, Appointment, db
from sqlalchemy import or_, func
from datetime import datetime, timedelta
from sqlalchemy import or_

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/available-slots')
@login_required
def available_slots():
    doctor_id = request.args.get('doctor_id', type=int)
    date_str = request.args.get('date', type=str)
    
    if not doctor_id or not date_str:
        return jsonify({"error": "doctor_id and date required"}), 400
        
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
        
    # In a real scenario, you'd calculate slots based on doctor's available_time_start and end,
    # and subtract existing appointments. For this demo, we'll return a static list 
    # and just remove booked ones.
    
    # Mock slots
    all_slots = ["09:00:00", "09:30:00", "10:00:00", "10:30:00"]
    
    booked = Appointment.query.filter_by(
        doctor_id=doctor_id, 
        appointment_date=date_str
    ).all()
    
    booked_times = [str(a.appointment_time) for a in booked]
    available = [s for s in all_slots if s not in booked_times]
    
    return jsonify({"slots": available})

@api_bp.route('/patient-search')
@login_required
def patient_search():
    query = request.args.get('query', type=str)
    if not query:
        return jsonify({"patients": []})
        
    patients = Patient.query.filter(or_(
        Patient.first_name.ilike(f'%{query}%'),
        Patient.last_name.ilike(f'%{query}%'),
        Patient.phone.ilike(f'%{query}%')
    )).all()
    
    return jsonify({
        "patients": [{"id": p.id, "name": f"{p.first_name} {p.last_name}", "phone": p.phone} for p in patients]
    })

@api_bp.route('/dashboard-stats')
@login_required
def dashboard_stats():
    # Get patient registrations grouped by month for the last 6 months
    today = datetime.today()
    labels = []
    data = []
    
    for i in range(5, -1, -1):
        target_month = (today.month - i - 1) % 12 + 1
        target_year = today.year + ((today.month - i - 1) // 12)
        
        # Simple string matching or sqlalchemy extract for month
        # In SQLite, we can use strftime
        month_str = f"{target_year}-{target_month:02d}"
        
        count = Patient.query.filter(func.strftime('%Y-%m', Patient.created_at) == month_str).count()
        
        labels.append(datetime(target_year, target_month, 1).strftime('%b'))
        data.append(count)
        
    return jsonify({
        "labels": labels,
        "data": data
    })
