import random
import time
import multiprocessing
import os
from flask import Flask, jsonify, render_template, redirect, request, send_file, abort
from data.__all_models import *
from data import db_session
from flask_socketio import SocketIO, emit, send
from generation_code import Generation_code
from random import choice
import threading
import flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
used_img = []

# url_ngrok = "192.168.7.138:5000"
url_ngrok = "127.0.0.1:5000"
# url_ngrok = "192.168.1.119:5000"

operating_rooms = {}
generation_code = Generation_code()
picture_at_the_monitor = {}
tranclete = {
    "anime": "Аниме",
    "pixelart": "Пиксель-арт",
    "realism": "Реализм",
    "impressionism": "Импрессионизм"
}


def get_img_id(style: str) -> int:
    global used_img
    db_sess = db_session.create_session()
    imgs = list(db_sess.query(Img).join(Style).filter(Style.name == style))
    imgs = list(filter(lambda img: not img.id in used_img, imgs))
    if (len(imgs) != 0):
        img = choice(imgs)
    else:
        imgs = list(db_sess.query(Img).filter(Img.style == style))
        for img in imgs:
            used_img.remove(img.id)
        img = choice(list(db_sess.query(Img).join(Style).filter(Style.name == style)))
    used_img.append(img.id)
    return img.id


"""
событие socketio на подключения клиетов
"""


@socketio.on('connect_client')
def connect_client(message: str) -> None:
    if (message.split()[0] == "js"):
        print("js подключился")
        emit("connect_user", message.split()[1], broadcast=True)
    if (message.split()[0] == "c#"):
        print("c# подключился")
        emit("get_ngrok_url", url_ngrok, broadcast=True)
    print(f'{message}')


"""
событие socketio на сообщения пользователей
"""


@socketio.on('select_img', namespace='/')
def handle_message(message: str) -> None:
    global picture_at_the_monitor
    if (int(message.split()[1]) in operating_rooms and operating_rooms[int(message.split()[1])] is False):
        operating_rooms[int(message.split()[1])] = True
        print(f'Received message: {message}')
        picture_at_the_monitor[int(message.split()[1])] = get_img_id(message.split()[0])
        emit("SwitchImg", message, broadcast=True)
        time_load = random.randint(4, 8)
        emit("set_time", str(time_load) + " " + message.split()[1], broadcast=True)
        t2 = threading.Thread(target=load_img, args=(message.split()[1], time_load), daemon=True)
        t2.start()

    # emit('response', f'Message received: {message}', broadcast=True)


@app.route('/img/<path:filename>')
def get_anime_img(filename):
    print(filename)
    file_path = filename
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        abort(404)


@app.route(f"/34763475t7347834/admin")
def admin_main():
    return render_template("index0.html")


@app.route(f"/34763475t7347834/admin/<string:style>")
def admin_imgs(style: str):
    db = db_session.create_session()
    imgs = db.query(Img).join(Style).filter(Style.name == tranclete[style]).all()
    imgs = list(
        map(lambda x: {"id": x.id, "path": x.path}, list(imgs)[::-1]))
    return render_template("index1.html", imgs=imgs, style=style)


@app.route(f"/34763475t7347834/admin/add")
def add_picture():
    return render_template("index2.html")


@app.route("/34763475t7347834/admin/change_text_style/<string:style>")
def showing_text_change_form(style: str):
    db = db_session.create_session()
    text_style = db.query(StyleText).join(Style).filter(Style.name == tranclete[style]).first().text
    print(text_style)
    return render_template("index3.html", style=style, text_style=text_style)


@app.route(f"/34763475t7347834/admin/load", methods=['GET', 'POST'])
def load_img():
    if request.method == 'POST':
        style = request.form.get('answer')
        file = request.files['uploaded_file']
        db = db_session.create_session()
        last_el = db.query(Img).all()
        if (len(last_el) == 0):
            last_id = 0
        else:
            last_id = last_el[-1].id
        img = Img()
        img.style = db.query(Style).filter(Style.name == tranclete[style]).first().id
        img.path = f"img/{style}/{last_id + 1}.png"
        file.save(img.path)
        db.add(img)
        db.commit()
        db.close()
    return redirect("/34763475t7347834/admin")


@app.route(f"/34763475t7347834/admin/del/<int:id>", methods=['GET', 'POST'])
def del_img(id):
    print(f"id img = {id}")
    db = db_session.create_session()
    img = db.query(Img).filter(Img.id == id).first()
    if (img is None):
        abort(404)
    print(img)
    try:
        os.remove(img.path)
    except Exception as err:
        print(err)
        ...
    db.delete(img)
    db.commit()
    db.close()
    return jsonify({})


@app.route(f"/34763475t7347834/admin/change_text/<string:style>", methods=['GET', 'POST'])
def change_text(style: str):
    if request.method == 'POST':
        print(request.form.get("text"))
        db = db_session.create_session()
        style_text = db.query(StyleText).join(Style).filter(Style.name == tranclete[style]).first()
        style_text.text = request.form.get("text")
        db.commit()


    return redirect(f"/34763475t7347834/admin/{style}")


@app.route("/")
def test() -> flask.json:
    return redirect("/34763475t7347834/admin")


@app.route("/ngrok/<string:url>", methods=['GET', 'POST'])
def set_ngrok_url(url: str) -> flask.json:
    global url_ngrok
    print(url, 1)
    # url_ngrok = "192.168.7.138"
    url_ngrok = url
    return jsonify({

    })


@app.route("/get_code_connect")
def get_code_conncect() -> flask.json:
    global operating_rooms
    code = generation_code.get_code(5)
    operating_rooms[int(code)] = False
    print("новый код " + code
          )
    return jsonify({
        "Code": code
    })


@app.route("/musem/<int:code_screen>")
def interaction_pc(code_screen: int) -> "Response":
    print(code_screen)
    print(operating_rooms)
    return render_template('index.html')


@app.route("/get_img/<int:code_acceot>")
def send_img_to_wpf(code_acceot: int) -> str:
    global used_img
    db_sess = db_session.create_session()
    img = db_sess.query(Img).filter(Img.id == picture_at_the_monitor[code_acceot]).first()
    print(img.id)

    with open(f"./{img.path}", "rb") as file:
        bin_code = file.read()
    return bin_code


@app.route("/download")
def download():
    return render_template("loading.html")


def load_img(code: str, time_sleep: int) -> None:
    print("sleep ", time_sleep)
    time.sleep(time_sleep)
    print("проснулся")
    with app.app_context():
        send(code, namespace="/", broadcast=True)
    print("отправил")


@app.route("/get_text/<string:style>")
def get_text(style: str):
    db = db_session.create_session()
    text = db.query(StyleText).join(Style).filter(Style.name == tranclete[style]).first().text
    print(text)
    return jsonify({"Text": text})


def start() -> None:
    os.system("python server_host.py")


if __name__ == '__main__':
    db_session.global_init("db/database.db")
    process = multiprocessing.Process(target=start)
    process.start()
    socketio.run(app)
