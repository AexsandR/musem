import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class StyleText(SqlAlchemyBase):
    __tablename__ = "StyleText"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    style = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Style.id"))
    text = sqlalchemy.Column(sqlalchemy.String(length=420))
