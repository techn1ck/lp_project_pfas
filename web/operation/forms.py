from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, SelectMultipleField
from wtforms.validators import DataRequired


class OperationForm(FlaskForm):
    category = SelectField('Категория', validators=[DataRequired()])
    account = SelectField('Счет', validators=[DataRequired()], coerce=int)
    tags = SelectMultipleField('Теги', coerce=int)
    name = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание (опционально)')
    value = DecimalField('Сумма', validators=[DataRequired()])
    submit = SubmitField('Отправить')
    # дата операции
