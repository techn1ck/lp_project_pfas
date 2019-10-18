from flask_wtf import FlaskForm
from wtforms import TextField, StringField, SubmitField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Название категории', validators=[DataRequired()])
    description = TextField('Описание')
    parent_id = SelectField('Родительская категория')
    submit = SubmitField('Отправить')