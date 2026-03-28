from app import create_app, db
from app.models import User, Doctor, Patient, Appointment, Prescription, Billing
from datetime import date, datetime, timedelta
import random

app = create_app()

with app.app_context():
    # Drop and recreate all tables
    db.drop_all()
    db.create_all()

    print("Database synced.")

    # 1. Create Admins
    print("Creating Admins...")
    admin1 = User(username='admin', email='admin@hospital.com', role='admin')
    admin1.set_password('password123')
    admin2 = User(username='superadmin', email='superadmin@hospital.com', role='admin')
    admin2.set_password('password123')
    receptionist = User(username='receptionist1', email='rec@hospital.com', role='receptionist')
    receptionist.set_password('password123')

    db.session.add_all([admin1, admin2, receptionist])
    db.session.commit()

    # 2. Create Doctors
    print("Creating Doctors...")
    specializations = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'General Medicine']
    doctors = []
    for i, spec in enumerate(specializations):
        user = User(username=f'dr_{spec.lower()[:4]}', email=f'dr{i+1}@hospital.com', role='doctor')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        doctor = Doctor(
            user_id=user.id,
            specialization=spec,
            qualification='MBBS, MD',
            experience_years=random.randint(5, 25),
            consultation_fee=float(random.choice([100, 150, 200])),
            room_number=f'{random.randint(100, 500)}'
        )
        db.session.add(doctor)
        doctors.append(doctor)
    db.session.commit()

    # 3. Create Patients
    print("Creating Patients...")
    first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Heidi']
    last_names = ['Smith', 'Doe', 'Johnson', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson']
    blood_groups = ['A+', 'O+', 'B+', 'AB+', 'A-', 'O-']
    patients = []

    for i in range(20):
        b_date = date.today() - timedelta(days=random.randint(3000, 25000))
        patient = Patient(
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            date_of_birth=b_date,
            gender=random.choice(['Male', 'Female']),
            blood_group=random.choice(blood_groups),
            phone=f'555-{random.randint(1000,9999)}',
            address=f'{random.randint(1,999)} Main St, City',
        )
        db.session.add(patient)
        patients.append(patient)
    db.session.commit()

    # 4. Create Appointments & Prescriptions & Bills
    print("Creating Appointments & Related Data...")
    statuses = ['completed', 'scheduled', 'cancelled', 'no-show']
    
    for i in range(50):
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        appt_date = date.today() + timedelta(days=random.randint(-30, 15))
        
        # Random time between 9 AM and 5 PM
        h = random.randint(9, 16)
        m = random.choice([0, 30])
        appt_time = datetime.strptime(f'{h}:{m}', '%H:%M').time()
        
        status = 'completed' if appt_date < date.today() else random.choice(['scheduled', 'cancelled'])
        
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_date=appt_date,
            appointment_time=appt_time,
            status=status,
            symptoms='Fever and headache' if random.random() > 0.5 else 'Routine checkup'
        )
        db.session.add(appointment)
        db.session.commit()
        
        if status == 'completed':
            # Prescription
            prescript = Prescription(
                appointment_id=appointment.id,
                diagnosis='Viral Infection' if 'Fever' in appointment.symptoms else 'Healthy',
                medicines='[{"name": "Paracetamol", "dosage": "500mg", "duration": "3 days"}]',
                instructions='Rest and drink fluids'
            )
            db.session.add(prescript)
            
            # Bill
            bill = Billing(
                patient_id=patient.id,
                appointment_id=appointment.id,
                consultation_fee=doctor.consultation_fee,
                medicine_cost=25.0,
                other_charges=10.0,
                total_amount=doctor.consultation_fee + 35.0,
                payment_status='paid',
                payment_method=random.choice(['cash', 'card', 'insurance']),
                payment_date=datetime.combine(appt_date, appt_time),
                invoice_number=f"INV-{str(random.randint(10000, 99999))}"
            )
            db.session.add(bill)
            
    db.session.commit()
    print("Seeding completed successfully!")
    print("\nTest User Accounts: ")
    print("1. Admin: admin@hospital.com / password123")
    print("2. Doctor: dr1@hospital.com / password123")
    print("3. Receptionist: rec@hospital.com / password123")
