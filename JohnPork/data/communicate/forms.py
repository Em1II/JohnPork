from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField
from wtforms.validators import DataRequired, Email

class WriteAResponseForm(FlaskForm):

    response = StringField("Ответь", validators=[DataRequired()])
    

    submit = SubmitField('Отправить!')

class WriteALetterForm(FlaskForm):

    letter = StringField("Напиши комплементарное письмо", validators=[DataRequired()])
    

    submit = SubmitField('Отправить!')

