from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, HiddenField
from wtforms.validators import Required


class AccountForm(FlaskForm):
    name = StringField('name', validators = [Required()])
    description = StringField('description')
    currency = SelectField(u'currency', choices=[])
