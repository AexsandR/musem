import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Style(SqlAlchemyBase):
    __tablename__ = "Style"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
