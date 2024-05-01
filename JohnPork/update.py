import datetime
from data.users.models import User
def update_ranks(db):
    users = db.query(User).all()
    for user in users:
        user.set_position()
    db.commit()


print(str(datetime.datetime.now().strftime("%A")))