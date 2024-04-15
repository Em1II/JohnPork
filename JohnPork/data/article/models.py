import sqlalchemy
from ..db_session import SqlAlchemyBase
import datetime

class Article(SqlAlchemyBase):
    
    __tablename__ = "article"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    imgage = sqlalchemy.Column(sqlalchemy.LargeBinary)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer)
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    title = sqlalchemy.Column(sqlalchemy.String)

    def save(self, file):
        

