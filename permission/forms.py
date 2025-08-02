from flask_babel import gettext as _
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired


class PermissionForm(FlaskForm):
    role_id = IntegerField()
    action=StringField()


class RoleForm(FlaskForm):
    role_id = IntegerField()
    name=StringField(validators=[DataRequired()])
    description=StringField(validators=[DataRequired()])
    permissions = SelectMultipleField(coerce=int,validators=[DataRequired(message=_('At_Least_One_Permission'))])