#permission/views.py
import logging

from flask import render_template, flash, redirect, url_for
from flask_babel import gettext as _
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload, selectinload

from auth.models import User
from dbs import db
from permission import bp
from permission.decorators import admin_required, require_permission
from permission.forms import PermissionForm, RoleForm
from permission.models import Role, Permission

# Configure logging
logger = logging.getLogger(__name__)

@bp.route('/admin')
@login_required
@admin_required
def admin_panel():
    """Admin panel dashboard"""
    users = User.query.options(joinedload(User.roles)).all()
    roles=Role.query.options(selectinload(Role.permissions)).all()
    permissions=Permission.query.options(selectinload(Permission.roles)).all()
    logger.info(f'Admin panel accessed by user: {current_user.username}')
    return render_template('admin_panel.html',users=users,roles=roles,permissions=permissions)


@bp.route('/roles', methods=['GET'])
@login_required
@require_permission('manage_roles')
def manage_roles():
    """Manage roles page"""
    logger.info(f'Roles management accessed by user: {current_user.username}')
    roles = Role.query.all()
    permissions=Permission.query.all()
    form=RoleForm()
    return render_template('manage_roles.html', roles=roles,permissions=permissions,form=form)


@bp.route('/roles/add', methods=['POST'])
@login_required
@require_permission('manage_roles')
def add_role():
    """Add new role"""
    form = RoleForm()
    form.permissions.choices = [(p.id, p.name) for p in Permission.query.all()]
    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)
        selected_permissions = Permission.query.filter(Permission.id.in_(form.permissions.data)).all()
        role.permissions = selected_permissions
        db.session.add(role)
        db.session.commit()
        logger.info(f'Role added: {role.name} by user: {current_user.username}')
        flash(_('Role_added'), 'success')
        return redirect(url_for('permission.manage_roles'))
    else:
        flash(_('Form_validation_failed'), 'error')
        permissions = Permission.query.all()
        roles = Role.query.all()
        return render_template('manage_roles.html',form=form,permissions=permissions,roles=roles)


@bp.route('/roles/<int:role_id>', methods=['GET'])
@login_required
@require_permission('manage_roles')
def view_role(role_id):
    """Add new role"""
    role = Role.query.options(selectinload(Role.permissions)).get_or_404(role_id)
    permissions = Permission.query.all()
    form = RoleForm()
    return render_template('edit_role.html', form=form, role=role,permissions=permissions, title=_('Edit_Role'))

@bp.route('/roles/<int:role_id>/edit', methods=['POST'])
@login_required
@require_permission('manage_roles')
def edit_role(role_id):
    """Edit existing role"""
    role = Role.query.options(selectinload(Role.permissions)).get_or_404(role_id)
    permissions = Permission.query.all()
    form = RoleForm()
    form.permissions.choices = [(p.id, p.name) for p in Permission.query.all()]
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        selected_permissions = Permission.query.filter(Permission.id.in_(form.permissions.data)).all()
        role.permissions = selected_permissions
        db.session.commit()
        logger.info(f'Role modified: {role.name} by user: {current_user.username}')
        flash(_('Role_modified'), 'success')
        return redirect(url_for('permission.manage_roles'))
    else:
        return render_template('edit_role.html', form=form, role=role,permissions=permissions, title=_('Edit_Role'))

@bp.route('/roles/<int:role_id>/delete', methods=['POST'])
@login_required
@require_permission('manage_roles')
def delete_role(role_id):
    """Delete role"""
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    logger.info(f'Role deleted: {role.name} by user: {current_user.username}')
    flash(_('Role_deleted'), 'success')
    return redirect(url_for('permission.manage_roles'))

@bp.route('/users')
@login_required
@require_permission('manage_users')
def manage_users():
    """Manage users page"""
    logger.info(f'Users management accessed by user: {current_user.username}')
    users = User.query.options(joinedload(User.roles)).all()
    roles = Role.query.all()
    form = PermissionForm()
    return render_template('manage_users.html', users=users,roles=roles, form=form)

@bp.route('/users/<int:user_id>/roles', methods=['GET', 'POST'])
@login_required
@require_permission('manage_users')
def manage_user_roles(user_id):
    """Manage user roles"""
    user = User.query.get_or_404(user_id)
    form = PermissionForm()
    # Populate role choices
    form.role_id.choices = [(r.id, r.name) for r in Role.query.all()]
    if form.validate_on_submit():
        role = Role.query.get(form.role_id.data)
        print(form.action)
        if role:
            if form.action and form.action.data=='remove':
                user.remove_role(role)
            else:
                user.add_role(role)
            db.session.commit()
            logger.info(f'Role {role.name} assigned to user {user.username} by {current_user.username}')
            flash(_('Role_assigned_to_user').format(role_name=role.name, username=user.username), 'success')
        return redirect(url_for('permission.manage_users', user_id=user_id))
    return render_template('manage_users.html', user=user, form=form)

@bp.route('/users/<int:user_id>/roles/<int:role_id>/remove', methods=['POST'])
@login_required
@require_permission('manage_users')
def remove_user_role(user_id, role_id):
    """Remove role from user"""
    user = User.query.get_or_404(user_id)
    role = Role.query.get_or_404(role_id)
    
    user.remove_role(role)
    db.session.commit()
    logger.info(f'Role {role.name} removed from user {user.username} by {current_user.username}')
    flash(_('Role_removed_from_user').format(role_name=role.name, username=user.username), 'success')
    return redirect(url_for('permission.manage_user_roles', user_id=user_id))

@bp.route('/init')
@login_required
@admin_required
def init_permissions():
    """Initialize permissions and roles"""
    try:
        # Create permissions
        permissions = [
            Permission(name='create_book', description='create_book'),
            Permission(name='edit_book', description='edit_book'),
            Permission(name='delete_book', description='delete_book'),
            Permission(name='view_books', description='view_books'),
            Permission(name='admin_panel', description='admin_panel'),
            Permission(name='manage_users', description='manage_users'),
            Permission(name='manage_roles', description='manage_roles'),
        ]
        
        for permission in permissions:
            if not Permission.query.filter_by(name=permission.name).first():
                db.session.add(permission)
        
        # Create roles
        user_role = Role(name='user', description='user')
        admin_role = Role(name='admin', description='admin')
        
        if not Role.query.filter_by(name='user').first():
            db.session.add(user_role)
        if not Role.query.filter_by(name='admin').first():
            db.session.add(admin_role)
        
        db.session.commit()
        
        # Assign permissions to roles
        user_role = Role.query.filter_by(name='user').first()
        admin_role = Role.query.filter_by(name='admin').first()
        
        if user_role and admin_role:
            # User role gets basic permissions
            view_books_perm = Permission.query.filter_by(name='view_books').first()
            if view_books_perm:
                user_role.add_permission(view_books_perm)
            
            # Admin role gets all permissions
            for permission in Permission.query.all():
                admin_role.add_permission(permission)
        
        db.session.commit()
        logger.info('Permissions and roles initialized successfully')
        flash(_('Init_successful'), 'success')
        
    except Exception as e:
        logger.error(f'Initialization failed: {str(e)}')
        flash(_('Init_failed').format(error=str(e)), 'error')
        db.session.rollback()
    
    return redirect(url_for('permission.admin_panel'))
