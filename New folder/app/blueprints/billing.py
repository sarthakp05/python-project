from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required
from app.decorators import role_required
from app.models import Billing, Appointment, Patient, db
from app.forms import BillingForm
import uuid
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

billing_bp = Blueprint('billing_bp', __name__)

@billing_bp.route('/', methods=['GET'])
@login_required
@role_required(['admin', 'receptionist'])
def list_bills():
    bills = Billing.query.order_by(Billing.payment_date.desc()).all()
    return render_template('billing/list.html', bills=bills)

@billing_bp.route('/generate/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'receptionist'])
def generate_bill(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check if bill already exists
    if appointment.billing:
        flash("Bill already generated for this appointment.", "warning")
        return redirect(url_for('billing_bp.list_bills'))
        
    form = BillingForm()
    
    if request.method == 'GET':
        form.consultation_fee.data = appointment.doctor.consultation_fee
        
    if form.validate_on_submit():
        total = (form.consultation_fee.data or 0) + (form.medicine_cost.data or 0) + (form.other_charges.data or 0)
        
        bill = Billing(
            patient_id=appointment.patient_id,
            appointment_id=appointment.id,
            consultation_fee=form.consultation_fee.data,
            medicine_cost=form.medicine_cost.data,
            other_charges=form.other_charges.data,
            total_amount=total,
            payment_status=form.payment_status.data,
            payment_method=form.payment_method.data,
            payment_date=datetime.utcnow() if form.payment_status.data != 'pending' else None,
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}"
        )
        db.session.add(bill)
        db.session.commit()
        flash("Bill generated successfully.", "success")
        return redirect(url_for('billing_bp.list_bills'))
        
    return render_template('billing/form.html', form=form, appointment=appointment)

@billing_bp.route('/print/<int:id>')
@login_required
@role_required(['admin', 'receptionist'])
def print_bill(id):
    bill = Billing.query.get_or_404(id)
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, 750, "MedCore HMS - Patient Invoice")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 720, f"Invoice Number: {bill.invoice_number}")
    p.drawString(50, 700, f"Date: {bill.payment_date.strftime('%Y-%m-%d') if bill.payment_date else 'Pending'}")
    
    p.drawString(50, 660, f"Patient Name: {bill.patient.first_name} {bill.patient.last_name}")
    p.drawString(50, 640, f"Consulting Doctor: Dr. {bill.appointment.doctor.user.username}")
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 590, "Charges Detail:")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 560, f"Consultation Fee: ${bill.consultation_fee:.2f}")
    p.drawString(50, 540, f"Medicine Cost: ${bill.medicine_cost:.2f}")
    p.drawString(50, 520, f"Other Charges: ${bill.other_charges:.2f}")
    
    p.line(50, 500, 300, 500)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 470, f"Total Amount: ${bill.total_amount:.2f}")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 440, f"Payment Method: {bill.payment_method.capitalize() if bill.payment_method else 'N/A'}")
    p.drawString(50, 420, f"Payment Status: {bill.payment_status.capitalize()}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=False, download_name=f"invoice_{bill.invoice_number}.pdf", mimetype='application/pdf')
