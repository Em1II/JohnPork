from flask import Flask, redirect, render_template, request, jsonify
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users.models import User
import os
from PIL import Image
import time
import flask
from data.users.forms import LoginForm, RegisterForm, EditForm, AppointmentForm
from data.communicate.forms import WriteALetterForm, WriteAResponseForm
from data.communicate.models import Dialog
from data.article.models import Article
from data.article.forms import CreateAnArticleForm
from scripts import getNameById, prettyTime, getaPorkSong
import datetime
from random import randint
import json

blueprint = flask.Blueprint(
    'JoPo_api',
    __name__,
    template_folder='templates'
)
quotes = [["Не кладите все яйца в одну корзину, если вы не свинья с очень большой корзиной", "Дж. Порк, 2013г"], 
          ["Когда жизнь подбрасывает вам лимоны, продайте их и наймите еще больше свиней", "Дж. Порк, 2011г"], 
          ["Инвестируйте в свиней, а не в свиней в мешке", "Дж. Порк, 2008г"], 
          ["Мое правило номер один: никогда не доверяй свинье, которая носит галстук", "Дж. Порк, 1991г"], 
          ["Porks - это свиная сила, с которой нужно считаться", "Дж. Порк, 2001г"], 
          ["Если у вас есть порки, вам не нужны деньги", "Дж. Порк, 2004г"], 
          ["Я не криптомиллионер. Я свино-миллионер", "Дж. Порк, 2021г"], 
          ["В мире криптовалют свиньи правят балом", "Дж. Порк, 2024г"], 
          ["Не будьте свиньей, которая продаст своих порков за пару трюфелей", "Дж. Порк, 2019г"], 
          ["Лучший способ разбогатеть - это инвестировать в свиней и свиные фьючерсы", "Дж. Порк, 2015г"], 
          ["Если вы хотите жить как свинья, вам нужно думать как свинья", "Дж. Порк, 2017г"], 
          ["Мир - это моя свиная площадка", "Дж. Порк, 2012г"], 
          ["Я не боюсь испачкаться. В конце концов, я свинья", "Дж. Порк, 2019г"], 
          ['Хрюканье - это мой способ сказать: "Я ваш верховный повелитель"', "Дж. Порк, 2024г"], 
          ["Следуйте за мной, и я приведу вас к свиному раю", "Дж. Порк, 2012г"], 
          ]
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SoWeakMeUp228'
app.config['ARTICLE_UPLOAD_FOLDER'] = "static/article"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "jfif"])


app.jinja_env.globals.update(getNameById=getNameById, prettyTime=prettyTime, getaPorkSong=getaPorkSong)
login_manager = LoginManager()
login_manager.init_app(app)
@blueprint.route('/api/Get-Pork-Song')
def get_PorkSong():
    try:
        with open("avicii.json", encoding='utf-8') as avc:
            a = dict(json.loads(avc.read()))
            f = int(time.strftime("%M"))
            m = f - f % 10
            dt = int(time.strftime("%d"))
            mod = len(a) - 1
            res = list(a.keys())[((m + dt) * 12 + 7) % mod]
            return jsonify({"response": [a[res], res]}) 
    except:

        return jsonify({"response":"Error"})


def allowed_files(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
def get_extansion(filename):
    return filename.rsplit(".", 1)[1].lower()
def upload_file_to_article(files, name):
    if "image" not in files:
        return str(files)
    file = files["image"]
    if file.filename == "":
        return "None2"
    
    if file and allowed_files(file.filename):
        filename = name + "." + get_extansion(file.filename)
        
        
        file.save(os.path.join(app.config["ARTICLE_UPLOAD_FOLDER"], filename))
        f = Image.open(os.path.join(app.config["ARTICLE_UPLOAD_FOLDER"], filename))
        if f.size[0] <= 600 or f.size[1] < 400:
            if f.size[0] < f.size[1]:
                f = f.resize((600, int(f.size[1] * (600 / f.size[0]))), Image.LANCZOS)
            else:
                f = f.resize(int((f.size[0] * (400 / f.size[1])), 400), Image.LANCZOS)
        f.save(os.path.join(app.config["ARTICLE_UPLOAD_FOLDER"], filename))
        return filename
    return "None3"
def get_last_dialog(id):
    db = db_session.create_session()
    dialogs = db.query(Dialog).filter(Dialog.sender_id == id, Dialog.response_date != None).all()
    obj = quotes[randint(0, len(quotes) - 1)]
    message, out = obj[0], obj[1]
    if dialogs:
        dialogs.sort(key=lambda a: a.response_date, reverse=True)
        dialog = dialogs[0]
        message, out = dialog.response, " Дж. Порк в ответ на ваше последнее письмо"
    
    return message, out
def get_news(amount):
    db = db_session.create_session()
    news = db.query(Article).all()
    news.sort(key=lambda a: a.creation_date, reverse=True)
        
    return news[:amount]


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)
@app.route('/', methods=["GET", "POST"])
def index():
    session = db_session.create_session()
    if current_user.is_authenticated:
        message, out = get_last_dialog(current_user.id)
        if message == None:
            obj = quotes[randint(0, len(quotes) - 1)]
            message, out = obj[0], obj[1]
    else:
        obj = quotes[randint(0, len(quotes) - 1)]
        message, out = obj[0], obj[1]
    news = session.query(Article).all()
    
    data = {
        'title': 'Главная',
        "message": message,
        "outmessage": out,
        "news":news,
        
    }

    form = WriteALetterForm()
    if form.validate_on_submit() and request.method == "POST":
        user = session.query(User).filter(User.id == current_user.id).first()
        dialog = Dialog()
        dialog.sender_id = user.id
        dialog.letter = form.letter.data
        session.add(dialog)
        session.commit()
        return redirect("/#social")
    return render_template('index.html', data=data, form=form, title="Главная")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):

            login_user(user, remember=form.remember_me.data)
            return redirect('/')

        return render_template('login.html', title='Авторизация', message='Вы не правильно ввели пароль', form=form)
    return render_template('login.html', title='Авторизация прервана по неустановленной причине',  form=form)
@app.route("/down.exe")
def down():
    return render_template("down.html")
@app.route("/down")
def okdown():
    return render_template("jellydown.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.rank = 4
        user.set_password(form.password.data)
        user.set_position()
        session.add(user)
        session.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')

    return render_template('register.html', title='Авторизация прервана по неустановленной причине', form=form)
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    db = db_session.create_session()
    user = db.query(User).filter(User.id == current_user.id).first()
    
    form = EditForm()
    if form.validate_on_submit():
        user.name = form.name.data if form.name.data != None else user.name.data
        user.age = form.age.data if form.age.data != None else user.age.data
        db.commit()
        return redirect("/account")

        
    
    return render_template('account.html', title='Аккаунт', user=user, form=form)
@app.route("/response", methods=["GET", "POST"])
@login_required
def response():
    db = db_session.create_session()
    waiting_for_response = db.query(Dialog).filter(Dialog.done == False).all()
    
    for dialog in waiting_for_response:
        form = WriteAResponseForm()
        if form.validate_on_submit():
            dialog.done = True
            dialog.response_date = datetime.datetime.now()
            dialog.responser_id = current_user.id
            dialog.response = form.response.data
            db.add(dialog)
            db.commit()
            return redirect("/response")
    
    if waiting_for_response:
        return render_template("/response.html", requests=waiting_for_response, form=form, status=1)
    return render_template("/response.html", status=0, message="Писем нет", title="Ответить")

@app.route("/appointment", methods=["POST", "GET"])
@login_required
def appointment():
    db = db_session.create_session()
    form = AppointmentForm()
    if form.validate_on_submit() and form.rank.data != "------":
        email = form.email.data
        rank = form.rank.data
        user = db.query(User).filter(User.email == email).first()
        user.rank = rank
        user.position = user.get_position()
        db.commit()
        return redirect("/appointment")
        

    return render_template("appointment.html", form=form, title="Назначение")
@app.route("/write-an-article", methods=["POST", "GET"])
@login_required
def write_an_article():
    db = db_session.create_session()
    form = CreateAnArticleForm()
    if form.validate_on_submit() and request.method == "POST":
        if db.query(Article).all():
            name = str(max(db.query(Article).all(), key=lambda a: a.id).id + 1 + 10 ** randint(1, 18))
        else:
            name = "60"
        res = upload_file_to_article(request.files, name)
        article = Article()
        article.image = res
        article.text = form.text.data
        article.title = form.title.data
        article.creator_id = current_user.id
        db.add(article)
        db.commit()
        return redirect("/write-an-article")
    return render_template("write.html", form=form, title="Написать")


@app.route("/article/<int:id>")
def article(id):
    db = db_session.create_session()
    article = db.query(Article).filter(Article.id == id).first()
    return render_template("/article.html", title=article.title, article=article)























def main():
    db_session.global_init("db/JohnPork.db")
    app.register_blueprint(blueprint)
    app.run(port=8080, debug=True)

 


if __name__ == '__main__':

    main()
    
    

