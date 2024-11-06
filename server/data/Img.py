import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Img(SqlAlchemyBase):
    __tablename__ = "img"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, unique=True)
    style = sqlalchemy.Column(sqlalchemy.String)
    info = orm.relationship("Img_tg", uselist=False, back_populates='img')