import sqlalchemy
import datetime

from ..db_session import SqlAlchemyBase

class Dialog(SqlAlchemyBase):
    __tablename__ = 'dialogs'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    
    responser_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    letter = sqlalchemy.Column(sqlalchemy.String, )
    response = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    done = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    request_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    response_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

