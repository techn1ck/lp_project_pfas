from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, HiddenField
from wtforms.validators import Required

class AccountForm(FlaskForm):
#    id = HiddenField('id')
#    id_user = HiddenField('id_user')
    name = StringField('name', validators = [Required()])
    description = StringField('description')
    currency = SelectField(u'currency', choices=[('1', 'Рубль'), ('2', 'Доллар'), ('3', 'Евро')])
