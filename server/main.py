import os
import time

from flask import *
from flask import render_template
from data.__all_models import *
import setting
from data import db_session
from flask_socketio import SocketIO, send
from multiprocessing import Process

app = Flask(__name__)
app.config['SECRET_KEY'] = setting.SECRET_KEY
socket = SocketIO(app)
used_img = set()
code_access = 0


@socket.on('message')
def handlerMsg(data: str) -> None:
    print(type(data))
    send("123123")
    print(f">> {data}")


@app.route("/")
def main_page() -> None:
    db_sess = db_session.create_session()
    # qwe = Img_tg()
    # for i in range(3):
    #     img = Img()
    #     img.style = "cyberpank"
    #     img.path = f"server/img/cyberpank/{i + 1}.jpg"
    #     db_sess.add(img)
    # for i in range(4, 7):
    #     img = Img()
    #     img.style = "anime"
    #     img.path = f"server/img/anime/{i}.jpg"
    #     db_sess.add(img)
    # qwe.id_img = 1
    # qwe.code = 23
    # db_sess.add(qwe)
    # db_sess.commit()
    return render_template("index0.html");


@app.route("/<int:code_img>")
def interaction_pc(code_img: int) -> None:
    db_sess = db_session.create_session()
    answer = {
        "code": 404,
        "path": ""
    }
    img = db_sess.query(Img_tg).filter(Img_tg.code == code_img).first()
    print(img)
    if (not (img is None)):
        answer["code"] = 200
        answer["path"] = img.img.path

    return jsonify(answer)


@app.route("/test")
def interactioan_pc() -> None:
    with open("C:/Users/borov/musem/server/img/anime/6.jpg", "rb") as file:
        bin_code = file.read()
    return bin_code



def start_bot():
    os.system("python ../bot/main.py")


if __name__ == '__main__':
    db_session.global_init("db/database.db")
    proc = Process(target=start_bot)
    proc.start()
    socket.run(app, host="192.168.1.147", port=8080, allow_unsafe_werkzeug=True)
