from functools import wraps

from flask import flash, redirect, url_for
from flask_babel import gettext as _
from flask_login import current_user


def require_permission(permission_name):
    """Decorator that requires specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash(_('Please_login_first'), 'warning')
                return redirect(url_for('auth.login'))
            
            # Check if user has the required permission
            for role in current_user.roles:
                for permission in role.permissions:
                    if permission.name == permission_name:
                        return f(*args, **kwargs)
            
            flash(_('No_permission'), 'error')
            return redirect(url_for('auth.login'))
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator that requires admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash(_('Please_login_first'), 'warning')
            return redirect(url_for('auth.login'))
        
        # Check if user has admin role
        for role in current_user.roles:
            if role.name == 'admin':
                return f(*args, **kwargs)
        
        flash(_('Admin_required'), 'error')
        return redirect(url_for('auth.login'))
    return decorated_function 