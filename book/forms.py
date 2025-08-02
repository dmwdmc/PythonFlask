from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
