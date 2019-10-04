from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, HiddenField
from wtforms.validators import Required


class AccountForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators = [Required()])
    description = StringField('description')
    id_currency = SelectField('id_currency')
