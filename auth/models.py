from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dbs import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    roles = db.relationship('Role', secondary='user_roles', backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name):
        """Check if user has specific permission"""
        for role in self.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return False

    def has_role(self, role_name):
        """Check if user has specific role"""
        return any(role.name == role_name for role in self.roles)

    def add_role(self, role):
        """Add role to user"""
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        """Remove role from user"""
        if role in self.roles:
            self.roles.remove(role)

    def __repr__(self):
        return f'<User {self.username}>'