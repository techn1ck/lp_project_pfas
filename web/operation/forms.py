from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, SelectMultipleField, DateField, HiddenField
from wtforms.validators import DataRequired


class OperationForm(FlaskForm):
    id = HiddenField('id')
    id_cat = SelectField('Категория', validators=[DataRequired()])
    id_account = SelectField('Счет', validators=[DataRequired()], coerce=int)
    tags = SelectMultipleField('Теги', coerce=int)
    name = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание (опционально)')
    value = DecimalField('Сумма', validators=[DataRequired()])
    creation_time = DateField('Дата операции')
    submit = SubmitField('Отправить')


class OperationsFilterForm(FlaskForm):
    date_from = DateField('Дата с')
    date_to = DateField('Дата по')
    filter_id_cat = SelectField('Категория')
    filter_id_account = SelectField('Счет')
    filter = SubmitField('Отфильтровать')
