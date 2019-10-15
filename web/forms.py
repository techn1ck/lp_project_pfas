from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, DecimalField, SelectMultipleField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Название счета', validators=[DataRequired()])
    description = TextField('Описание')
    id_currency = SelectField('Валюта счета')
    submit = SubmitField('Отправить')


class CategoryForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Название категории', validators=[DataRequired()])
    description = TextField('Описание')
    parent_id = SelectField('Родительская категория')
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    telegram = StringField('Логин телеграм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить?', default=True)
    submit = SubmitField('Войти')


class OperationForm(FlaskForm):
    category = SelectField('Категория', validators=[DataRequired()])
    account = SelectField('Счет', validators=[DataRequired()], coerce=int)
    tags = SelectMultipleField('Теги', coerce=int)
    name = StringField('Название', validators=[DataRequired()])
    description = TextField('Описание (опционально)')
    value = DecimalField('Сумма', validators=[DataRequired()])
    submit = SubmitField('Отправить')
    # дата операции


class TagForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Название', validators=[DataRequired()])
    description = TextField('Описание')
    submit = SubmitField('Отправить')
