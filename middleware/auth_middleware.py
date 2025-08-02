# middleware/auth_middleware.py
from functools import wraps
from flask import request, redirect, url_for, flash
from flask_login import current_user
from flask_babel import gettext as _


def require_auth():
    """Decorator to require authentication for routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash(_('Please_login_first'), 'warning')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_login_status(app):
    """Middleware to check login status for all requests"""
    # Define public routes that don't require authentication
    public_routes = [
        'auth.login',
        'auth.register',
        'static'
    ]
    
    @app.before_request
    def before_request():
        # Skip middleware for static files
        if request.endpoint == 'static':
            return None
            
        # Check if the current route is public
        if request.endpoint:
            is_public = any(route in request.endpoint for route in public_routes)
            
            # If not public and user is not authenticated, redirect to login
            if not is_public and not current_user.is_authenticated:
                # Store the original URL to redirect back after login
                next_page = request.url
                return redirect(url_for('auth.login', next=next_page))
        else:
            return redirect(url_for('auth.login'))
        return None


def init_auth_middleware(app):
    """Initialize authentication middleware"""
    check_login_status(app) 