from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField('Электронная почта:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField('Войти!')

class RegisterForm(FlaskForm):

    email = EmailField('Электронная почта:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    name = StringField("Имя:", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField('Зарегистрироваться!')

class EditForm(FlaskForm):

    name = StringField("Имя", validators=[DataRequired()])
    age = IntegerField("Возраст")

    submit = SubmitField('Изменить!')


class AppointmentForm(FlaskForm):
    email = EmailField("Электронная почта", validators=[DataRequired(), Email()])
    rank = SelectField('Должность', choices=[(None, "------"), (3, "Писатель"), (2, "Админ"), (4, "Читатель"), (1, "Верховный Повелитель")])
    submit = SubmitField('Применить')
