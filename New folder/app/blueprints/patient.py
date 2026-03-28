from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required
from app.decorators import role_required
from app.models import Patient, db
from app.forms import PatientForm
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/', methods=['GET'])
@login_required
@role_required(['admin', 'doctor', 'receptionist'])
def list_patients():
    blood_group = request.args.get('blood_group')
    query = Patient.query
    if blood_group:
        query = query.filter_by(blood_group=blood_group)
    patients = query.all()
    return render_template('patient/list.html', patients=patients, current_filter=blood_group)

@patient_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'receptionist'])
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            blood_group=form.blood_group.data,
            phone=form.phone.data,
            address=form.address.data,
            emergency_contact=form.emergency_contact.data,
            medical_history=form.medical_history.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully', 'success')
        return redirect(url_for('patient_bp.list_patients'))
    return render_template('patient/form.html', form=form, title="Add Patient")

@patient_bp.route('/<int:id>', methods=['GET'])
@login_required
def view_patient(id):
    patient = Patient.query.get_or_404(id)
    return render_template('patient/view.html', patient=patient)

@patient_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'doctor', 'receptionist'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm(obj=patient)
    
    if form.validate_on_submit():
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.date_of_birth = form.date_of_birth.data
        patient.gender = form.gender.data
        patient.blood_group = form.blood_group.data
        patient.phone = form.phone.data
        patient.address = form.address.data
        patient.emergency_contact = form.emergency_contact.data
        patient.medical_history = form.medical_history.data
        
        db.session.commit()
        flash('Patient updated successfully', 'success')
        return redirect(url_for('patient_bp.view_patient', id=patient.id))
        
    return render_template('patient/form.html', form=form, title=f"Edit {patient.first_name} {patient.last_name}")

@patient_bp.route('/export/<int:id>')
@login_required
def export_profile(id):
    patient = Patient.query.get_or_404(id)
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Patient Profile - MedCore HMS")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 700, f"Patient Name: {patient.first_name} {patient.last_name}")
    p.drawString(50, 680, f"Patient ID: PT-{patient.id:04d}")
    p.drawString(50, 660, f"Blood Group: {patient.blood_group}")
    p.drawString(50, 640, f"Gender: {patient.gender}")
    p.drawString(50, 620, f"Phone: {patient.phone}")
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 580, "Medical History:")
    
    p.setFont("Helvetica", 12)
    text_object = p.beginText(50, 560)
    history_lines = (patient.medical_history or 'No medical history recorded.').split('\n')
    for line in history_lines:
        text_object.textLine(line)
    p.drawText(text_object)
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=False, download_name=f"patient_profile_{patient.id}.pdf", mimetype='application/pdf')
