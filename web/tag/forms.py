from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class TagForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание')
    submit = SubmitField('Отправить')
