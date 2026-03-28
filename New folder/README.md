# MedCore HMS - Hospital Management System

A comprehensive, production-ready Hospital Management System built with Flask, SQLAlchemy, and Bootstrap 5. It handles role-based access control, patient records, doctor scheduling, and billing management.

## Features

- **Role-Based Access Control**
  - **Admin**: Has full access, can view dashboard metrics, and manage users.
  - **Doctor**: Can view their schedule, and write prescriptions.
  - **Receptionist**: Dedicated dashboard for booking appointments and adding patients.
  
- **Patient Management**: Complete CRUD operations, export records visually, view medical histories.
- **Appointments**: Real-time slot checking simulation, conflict prevention, dynamic dropdowns.
- **Billing System**: Invoice generation, itemized billing (Consultation, Medicine).
- **Beautiful UI**: Built with Bootstrap 5, FontAwesome, DataTables, and custom CSS.

## Getting Started

Follow these steps to set up the system locally.

### Prerequisites

Ensure you have Python 3.8+ installed.

### Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize and Seed the Database:
   ```bash
   python seed.py
   ```
   *This drops existing tables, configures the database, and injects 50+ mock records for testing.*

4. Run the Application:
   ```bash
   python run.py
   ```

## Test Accounts

The `seed.py` will generate multiple test accounts to verify different roles:
- **Admin**: `admin@hospital.com` / `password123`
- **Doctor**: `dr1@hospital.com` / `password123`
- **Receptionist**: `rec@hospital.com` / `password123`
