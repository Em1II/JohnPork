from flask import Flask, redirect, render_template, request
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users.models import User
from data.users.forms import LoginForm, RegisterForm, EditForm, AppointmentForm
from data.communicate.forms import WriteALetterForm, WriteAResponseForm
from data.communicate.models import Dialog
import datetime

def getNameById(id):
    db = db_session.create_session()
    return db.query(User).filter(User.id == id).first().name


def prettyTime(time):
    weeekdaysRu = { "Monday":"Понедельник", "Tuesday":"Вторник", "Wednesday":"Среда", "Thursday":"Четверг", "Friday":"Пятница", "Saturday":"Суббота","Sunday":"Воскресенье"}
    WeekdayNowEng = time.strftime("%A")
    WeekdayNowRu = weeekdaysRu[WeekdayNowEng]
    date = time.strftime("%m-%d-%Y")
    ttime = time.strftime("%H:%M")




    return f"{date}, {WeekdayNowRu}, {ttime}"
