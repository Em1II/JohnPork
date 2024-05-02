import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
ranks = {'1': "Верховный Повелитель", '2': "Админ", '3': "Писатель", '4': "Читатель", 1: "Верховный Повелитель", 2: "Админ", 3: "Писатель", 4: "Читатель"}
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, default=226)
    position = sqlalchemy.Column(sqlalchemy.String, default="Читататель")
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    
    rank = sqlalchemy.Column(sqlalchemy.Integer)
    remember_me = sqlalchemy.Column(sqlalchemy.Boolean)


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    def set_position(self):
        self.position = ranks[self.rank]
    def get_position(self):
        return ranks[self.rank]
       
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def __repr__(self) -> str:
        return f' <Colonist> {self.id} {self.surname} {self.name}'
    
    




