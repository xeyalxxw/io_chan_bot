import telebot
import big_answers
import const

from datetime import datetime
from pygame import mixer

"""
print('Звук н-нада? (y/n)')
input_sound = input()
if input_sound == "y":
    sound = True
    print("Звук есть")
elif input_sound == "n":
    sound = False
    print("Звука нет")
else:
    sound = False
    print("Звука нету...")
print("______________________________________________________________________\n\n")
"""
sound = False

bot = telebot.TeleBot(const.token)

bot.send_message(const.main_chat_id, "Я запустилась!")

mixer.init()
mixer.music.load('sound.mp3')


# Логирование
def log(message, answer):
    if sound:
        mixer.music.play()

    print('\n{0} {1} {2} ({3}): {4}'.format(str(datetime.now())[:-7],
                                            message.from_user.first_name,
                                            message.from_user.last_name,
                                            str(message.from_user.id),
                                            message.text))
    print("Ответ: " + answer)


@bot.message_handler(commands=['stop_oi', 'start'])
def handle_text(message):
    user_id = message.from_user.id

    # /stop_oi
    if message.text == "/stop_oi":
        if user_id == const.admin_id:

            bot.send_message(message.chat.id,
                             "Я остановлена... Хозяин, только ты запусти меня поскорее! 😼")
            print("\n" + str(datetime.now()) + " Хозяин остановил меня (/stop_oi)")
            exit()
        else:
            answer = "Ты мне не хозяин!"
            bot.send_message(message.chat.id, answer)
            log(message, answer)

    # /start
    if message.text == "/start":
        if user_id == const.admin_id:
            answer = "Опять двадцать пять! Замучал девку! 😾"
            bot.send_message(message.chat.id, answer)
            log(message, answer)
        else:
            answer = big_answers.start_answer
            bot.send_message(message.chat.id, answer)
            answer = "*Длиииинная паста при команде /start*"
            log(message, answer)


@bot.message_handler(content_types=["sticker"])
def handle_docs_s(message):
    answer = (
        "ID этого стикера:\n{0}\nСмайл этого стикера: {1}\nРазмер этого стикера: {2} КБайт".format(
            str(message.sticker.file_id),
            message.sticker.emoji,
            (str(message.sticker.file_size/8192))[:4]))
    bot.send_message(message.chat.id, answer)
    message.text = "Стикер"
    log(message, answer)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Создаю новую переменную с коротким для того, чтобы каждый раз не писать огромные стоковые.
    user_id = message.from_user.id
    txt = message.text.lower()

    if user_id == const.admin_id:

        # Сравниваю с str.lower() для того, чтобы сообщения не были
        # зависимы от регистра, и код не получился таким громоздким.
        # --------------------------------------------------------------------- Admin's messages.

        if txt == "Привет".lower():
            answer = "Здравствуй, Хозяин!"
        elif txt == 'Ои'.lower():
            answer = "Да, хозяин? 😸"
        elif txt == 'Оичка'.lower():
            answer = "Мур! 😸"
        elif txt == 'Пизда'.lower():
            answer = "Мне не нравится, когда ты говоришь такие слова, бака! 😾"
        else:
            answer = "Не понимать... 😿"

            # --------------------------------------------------------------------- User's messages

    else:
        if txt.lower() == 'Привет':
            answer = "Писю на обед! 😼"
        elif message.text == '/start':
            answer = big_answers.start_answer
        elif txt == '/start'.lower():
            answer = big_answers.start_answer
        elif txt == 'Ои'.lower():
            answer = "М?"
        elif txt == 'Оичка'.lower():
            answer = "Мур! 😸"
        elif txt == 'Пизда'.lower():
            answer = "Мне не нравится, когда ты говоришь такие слова, бака! 😿"
        else:
            answer = "Не понимать... 😿"

    # Тут бот отвечает на сообщение юзера и логирует его сообщение и свой ответ.
    bot.send_message(message.chat.id, answer)
    log(message, answer)


# Тут скрипт постоянно посылает запрос на сервера Telegram для получения новых сообщений.
bot.remove_webhook()
bot.polling(none_stop=True, interval=0)
