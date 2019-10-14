from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, DecimalField, SelectMultipleField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators=[DataRequired()])
    description = TextField('description')
    id_currency = SelectField('id_currency')
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators=[DataRequired()])
    description = TextField('description')
    parent_id = SelectField('parent_id')
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    telegram = StringField('Логин телеграм', validators=[DataRequired()], default="mytg")
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить?')
    submit = SubmitField('Войти')


class OperationForm(FlaskForm):
    category = SelectField('Категория', validators=[DataRequired()], coerce=int)
    account = SelectField('Счет', validators=[DataRequired()], coerce=int)
    tags = SelectMultipleField('Теги', coerce=int)
    name = StringField('Название', validators=[DataRequired()])
    description = TextField('Описание (опционально)')
    value = DecimalField('Сумма', validators=[DataRequired()])
    submit = SubmitField('Отправить')
    # дата операции


class TagForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators=[DataRequired()])
    description = TextField('description')
    submit = SubmitField('Submit')
