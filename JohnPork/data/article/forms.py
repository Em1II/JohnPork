from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, TextAreaField, StringField
from wtforms.validators import data_required

class CreateAnArticleForm(FlaskForm):

    image = FileField("Картинка статьи", validators=[data_required()])
    text = TextAreaField("Содержание статьи", validators=[data_required()])
    title = StringField("Заголовок", validators=[data_required()])
    





    submit = SubmitField("Опубликовать!")