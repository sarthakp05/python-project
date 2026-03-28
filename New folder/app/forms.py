from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, IntegerField, DateField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[Optional()])
    blood_group = SelectField('Blood Group', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], validators=[Optional()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()])
    emergency_contact = StringField('Emergency Contact', validators=[Optional(), Length(max=100)])
    medical_history = TextAreaField('Medical History', validators=[Optional()])
    submit = SubmitField('Submit')

class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    appointment_date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    appointment_time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    symptoms = TextAreaField('Symptoms', validators=[Optional()])
    submit = SubmitField('Book Appointment')

class PrescriptionForm(FlaskForm):
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired()])
    medicines = TextAreaField('Medicines (JSON format)', validators=[DataRequired()]) # In real app, this should be field list
    instructions = TextAreaField('Instructions', validators=[Optional()])
    follow_up_date = DateField('Follow Up Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Save Prescription')

class BillingForm(FlaskForm):
    consultation_fee = FloatField('Consultation Fee', validators=[Optional(), NumberRange(min=0)])
    medicine_cost = FloatField('Medicine Cost', validators=[Optional(), NumberRange(min=0)])
    other_charges = FloatField('Other Charges', validators=[Optional(), NumberRange(min=0)])
    payment_method = SelectField('Payment Method', choices=[('cash', 'Cash'), ('card', 'Card'), ('insurance', 'Insurance')], validators=[DataRequired()])
    payment_status = SelectField('Payment Status', choices=[('pending', 'Pending'), ('paid', 'Paid'), ('partially_paid', 'Partially Paid')], validators=[DataRequired()])
    submit = SubmitField('Generate Bill')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password (leave blank to keep current)', validators=[Optional()])
    submit = SubmitField('Update Profile')

