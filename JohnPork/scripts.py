from data import db_session
from data.users.models import User

import requests

def getNameById(id):
    db = db_session.create_session()
    return db.query(User).filter(User.id == id).first().name
def getaPorkSong():
    link = "http://127.0.0.1:8080/api/Get-Pork-Song"
    d = requests.get(link).json()
    
    return f'Сейчас Джон слушает трек <<{d["response"][1]}>> исполнителя {d["response"][0]}' if d["response"] != "Error" else "Джон Порк сейчас ничего не слушает"

def prettyTime(time):
    if time == "null":
        return ""
    weeekdaysRu = { "Monday":"Понедельник", "Tuesday":"Вторник", "Wednesday":"Среда", "Thursday":"Четверг", "Friday":"Пятница", "Saturday":"Суббота","Sunday":"Воскресенье"}
    WeekdayNowEng = time.strftime("%A")
    WeekdayNowRu = weeekdaysRu[WeekdayNowEng]
    date = time.strftime("%m-%d-%Y")
    ttime = time.strftime("%H:%M")




    return f"{date}, {WeekdayNowRu}, {ttime}"
