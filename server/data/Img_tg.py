import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class Img_tg(SqlAlchemyBase):
    __tablename__ = "img_tg"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_img = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("img.id"))
    img = orm.relationship("Img", back_populates='info')
    code = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
