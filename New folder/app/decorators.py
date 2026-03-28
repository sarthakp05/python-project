from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(roles):
    """
    Decorator to restrict access to users with specific roles.
    Expects a list of allowed roles.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth_bp.login'))
            if current_user.role not in roles:
                flash("You don't have permission to access this page.", 'danger')
                # redirect based on their role
                if current_user.role == 'admin':
                    return redirect(url_for('admin_bp.dashboard'))
                elif current_user.role == 'doctor':
                    return redirect(url_for('doctor_bp.dashboard'))
                else:
                    return redirect(url_for('auth_bp.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
