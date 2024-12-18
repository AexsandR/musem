import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Img(SqlAlchemyBase):
    __tablename__ = "Img"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, unique=True)
    style = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Style.id"))
