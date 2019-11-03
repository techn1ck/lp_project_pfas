from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Название категории', validators=[DataRequired()])
    description = StringField('Описание')
    parent_id = SelectField('Родительская категория')
    submit = SubmitField('Отправить')
