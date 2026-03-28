from flask import Flask, render_template, request, jsonify
from config import Config
from .extensions import db, migrate, login_manager, mail

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Context processors
    @app.context_processor
    def inject_global_data():
        return {
            'app_name': 'HMS System',
            'unread_notifications': 0 # Placeholder for unread notifications count
        }

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    # Register Blueprints
    # Note: These will be defined in subsequent steps
    from .blueprints.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .blueprints.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from .blueprints.doctor import doctor_bp
    app.register_blueprint(doctor_bp, url_prefix='/doctor')

    from .blueprints.patient import patient_bp
    app.register_blueprint(patient_bp, url_prefix='/patient')

    from .blueprints.appointment import appointment_bp
    app.register_blueprint(appointment_bp, url_prefix='/appointment')

    from .blueprints.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from .blueprints.billing import billing_bp
    app.register_blueprint(billing_bp, url_prefix='/billing')

    from .blueprints.receptionist import receptionist_bp
    app.register_blueprint(receptionist_bp, url_prefix='/receptionist')

    # Root route
    @app.route('/')
    def index():
        from flask_login import current_user
        from flask import redirect, url_for
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin_bp.dashboard'))
            elif current_user.role == 'doctor':
                return redirect(url_for('doctor_bp.dashboard'))
            elif current_user.role == 'receptionist':
                return redirect(url_for('receptionist_bp.dashboard'))
            else:
                return redirect(url_for('auth_bp.login'))
        return redirect(url_for('auth_bp.login'))

    return app
