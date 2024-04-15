from flask import Flask, redirect, render_template, request
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users.models import User
from data.users.forms import LoginForm, RegisterForm, EditForm, AppointmentForm
from data.communicate.forms import WriteALetterForm, WriteAResponseForm
from data.communicate.models import Dialog
from data.article.models import Article
from data.article.forms import CreateAnArticleForm
from scripts import getNameById, prettyTime
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SoWeakMeUp228'
app.jinja_env.globals.update(getNameById=getNameById, prettyTime=prettyTime)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)
@app.route('/', methods=["GET", "POST"])
def index():
    data = {
        'title': 'Главная',
    }
    form = WriteALetterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        dialog = Dialog()
        dialog.sender_id = user.id
        dialog.letter = form.letter.data
        session.add(dialog)
        session.commit()
        return redirect("/#social")
    return render_template('index.html', data=data, form=form)

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
    return render_template("/response.html", status=0, message="Писем нет")

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
    if form.validate_on_submit():
        article = Article()
        article.imgage = form.image.meta
        article.text = form.text.data
        article.title = form.title.data
        article.creator_id = current_user.id
        db.add(article)
        db.commit()
        return redirect("/write-an-article")
    return render_template("write.html", form=form, title="Написать")








def main():
    db_session.global_init("db/JohnPork.db")

    app.run(debug=True, port=8080)

 


if __name__ == '__main__':

    main()
    

