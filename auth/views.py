#auth/views.py
import logging
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload
from flask_babel import gettext as _

from auth.forms import LoginForm, RegistrationForm
from auth.models import User
from dbs import db
from permission.models import Role
from auth import bp

# Configure logging
logger = logging.getLogger(__name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to books page
    if current_user.is_authenticated:
        return redirect(url_for('book.books'))
        
    form = RegistrationForm()
    logger.info('Registration form submitted')
    if form.validate_on_submit():
        # Check if username/email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()
        if existing_user:
            logger.warning(f'Registration failed: username or email already exists - {form.username.data}')
            flash(_('Username_or_email_exists'), 'error')
            return redirect(url_for('auth.register'))

        # Encrypt password and create user
        hashed_pwd = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_pwd
        )
        
        # Assign default role to new user
        default_role = Role.query.filter_by(name='user').first()
        if default_role:
            user.add_role(default_role)
            logger.info(f'Assigned default role "user" to new user: {user.username}')
        
        db.session.add(user)
        db.session.commit()
        logger.info(f'User registered successfully: {user.username}')
        flash(_('Registration_successful'), 'success')
        return redirect(url_for('auth.login'))
    else:
        logger.warning('Registration form validation failed')
    return render_template('register.html', form=form)

@bp.route('/login', methods=['POST'])
def login():
    # If user is already logged in, redirect to books page
    if current_user.is_authenticated:
        return redirect(url_for('book.books'))
        
    username = request.form.get('username')
    password = request.form.get('password')
    logger.info(f'Login attempt for user: {username}')
    
    # Optimization: Load user and roles in one query
    user = User.query.options(
        joinedload(User.roles)
    ).filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)  # Establish session
        logger.info(f'User logged in successfully: {username}')
        
        # Redirect to next page if specified, otherwise to books page
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        return redirect(url_for('book.books'))
    else:
        logger.warning(f'Login failed for user: {username}')
        flash(_('Invalid_credentials'), 'error')
        return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET'])
def loginPage():
    # If user is already logged in, redirect to books page
    if current_user.is_authenticated:
        return redirect(url_for('book.books'))
        
    form = LoginForm()
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logger.info(f'User logged out')
    logout_user()
    flash(_('Logged_out_successfully'), 'info')
    return redirect(url_for('auth.login'))
