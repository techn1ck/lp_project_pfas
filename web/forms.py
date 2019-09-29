from flask_wtf import FlaskForm
from wtforms import TextField, SelectField, StringField
from wtforms.validators import Required

class AccountForm(FlaskForm):
    name = StringField('name', validators = [Required()])
    description = TextField('description')
    currency = SelectField(u'currency', choices=[('1', 'Рубль'), ('2', 'Доллар'), ('3', 'Евро')])
