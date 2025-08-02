from dbs import db


# Permission table
class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Permission {self.name}>'

# Role table
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200))
    permissions = db.relationship('Permission', secondary='role_permissions', backref='roles')

    def __repr__(self):
        return f'<Role {self.name}>'

# Role-Permission association table
class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)

# User-Role association table
class UserRole(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)