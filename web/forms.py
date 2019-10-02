from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Логин телеграм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    #remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')