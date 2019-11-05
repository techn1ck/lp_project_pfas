from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Название счета', validators=[DataRequired()])
    description = StringField('Описание')
    id_currency = SelectField('Валюта счета')
    submit = SubmitField('Отправить')
