import json
import pprint

import requests
import setting
import telebot

token = setting.TOKEN
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name} ✌️")
    bot.send_message(message.chat.id, f"введи код с экрана")

@bot.message_handler(content_types='text')
def start_message(message):
    res = requests.get(setting.URL + message.text)
    if(res.status_code == 200):
        path = res.json()["path"]
        if(path != ""):
            with open("../" + path, "rb") as file:
                bin_code = file.read()
                bot.send_photo(message.from_user.id, photo=bin_code)
                return
    bot.send_message(message.chat.id, "ничего не нашел по вашему коду")
    bot.send_message(message.chat.id, "попробуйте другой код")


if __name__ == '__main__':
    print("bot запущен")
    bot.infinity_polling()
