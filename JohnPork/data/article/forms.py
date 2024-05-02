from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import data_required
from flask_wtf.file import FileField, FileAllowed, FileRequired
class CreateAnArticleForm(FlaskForm):

    image = FileField("Картинка статьи")
    text = TextAreaField("Содержание статьи", validators=[data_required()])
    title = StringField("Заголовок", validators=[data_required()])
    enctype="multipart/form-data"





    submit = SubmitField("Опубликовать!")