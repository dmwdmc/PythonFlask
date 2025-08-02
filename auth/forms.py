from flask_babel import gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField( validators=[DataRequired(message=_("Username_empty")),Length(min=3, max=25, message=_("Length_3_25_chars"))])
    email = StringField(validators=[DataRequired(),Email()])
    password = PasswordField(validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField(validators=[DataRequired(),EqualTo('password', message=_('Passwords_must_match'))])
