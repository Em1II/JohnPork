from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, length

class WriteAResponseForm(FlaskForm):

    response = TextAreaField("Ответь", validators=[DataRequired(), length(min=7, max=650)])
    

    submit = SubmitField('Отправить!')

class WriteALetterForm(FlaskForm):

    letter = TextAreaField("Напиши комплементарное письмо", validators=[DataRequired()])
    

    submit = SubmitField('Отправить!')

