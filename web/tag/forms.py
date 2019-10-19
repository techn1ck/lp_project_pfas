from flask_wtf import FlaskForm
from wtforms import TextField, StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class TagForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Название', validators=[DataRequired()])
    description = TextField('Описание')
    submit = SubmitField('Отправить')
