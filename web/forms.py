from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired


class AccountForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators = [DataRequired()])
    description = TextField('description')
    id_currency = SelectField('id_currency')
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name', validators = [DataRequired()])
    description = TextField('description')
    parent_id = SelectField('parent_id')
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    telegram = StringField('Логин телеграм', validators = [DataRequired()])
    password = PasswordField('Пароль', validators = [DataRequired()])
    remember_me = BooleanField('Запомнить?')
    submit = SubmitField('Войти')