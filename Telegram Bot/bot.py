import telebot
import datetime
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import json
import os
import pytz



TOKEN = '7413652825:AAG8WrPJAmMgLpJdbltVgVn_3Tsr0lnn3TY'
bot = telebot.TeleBot(TOKEN)

USERS_FILE = r"C:\Users\herob\PycharmProjects\TeleBot\Telegram-Bot\Telegram Bot\users.json"
USERS_DATA_FILE = r"C:\Users\herob\PycharmProjects\TeleBot\Telegram-Bot\Telegram Bot\users_data.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    print(f"Users saved to {USERS_FILE}: {users}")

users = load_users()
print(f"Loaded users from {USERS_FILE}: {users}")

def load_users_data():
    if os.path.exists(USERS_DATA_FILE):
        with open(USERS_DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

def save_users_data(users_data):
    with open(USERS_DATA_FILE, 'w') as f:
        json.dump(users_data, f)
    print(f"Users data saved to {USERS_DATA_FILE}: {users_data}")

users_data = load_users_data()
print(f"Loaded users data from {USERS_DATA_FILE}: {users_data}")

user_states = {}  # Словарь для хранения состояния пользователей

def set_commands(bot):
    commands = [
        types.BotCommand(command="/start", description="Запустить бота"),
        types.BotCommand(command="/help", description="Получить помощь"),
        types.BotCommand(command="/weight", description="Записать вес"),
        types.BotCommand(command="/height", description="Записать рост")
    ]
    bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def main(message):
    if message.chat.id not in users:
        users.append(message.chat.id)
        save_users(users)
        print(f"Added user {message.chat.id} to users list")

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Гаф")
    button2 = types.KeyboardButton("Мур")
    button3 = types.KeyboardButton("Записать активность")
    button4 = types.KeyboardButton("Посмотреть калории")
    menu.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'Привет, Звездочка', reply_markup=menu)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Команды:\n/start - начать\n/help - помощь\n/calories - посмотреть потраченные калории\n/weight - записать вес\n/height - записать рост')

@bot.message_handler(commands=['weight'])
def set_weight(message):
    chat_id = str(message.chat.id)
    user_states[chat_id] = 'awaiting_weight'
    print(f"User {chat_id} state set to awaiting_weight")  # Отладочное сообщение
    bot.send_message(chat_id, "Введите ваш вес в килограммах:")

@bot.message_handler(commands=['height'])
def set_height(message):
    chat_id = str(message.chat.id)
    user_states[chat_id] = 'awaiting_height'
    print(f"User {chat_id} state set to awaiting_height")  # Отладочное сообщение
    bot.send_message(chat_id, "Введите ваш рост в сантиметрах:")

@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_message(message):
    chat_id = str(message.chat.id)
    state = user_states.get(chat_id)
    print(f"User {chat_id} state: {state}")  # Отладочное сообщение для текущего состояния пользователя

    if message.chat.type == 'private':
        if message.text == 'Мур':
            bot.send_sticker(chat_id, 'CAACAgQAAxkBAAEMSDdmZtRD3_A_HPBaevXukKsDtu46cQAC3wgAAvFVgVFsqsmMvkACyDUE')
        elif message.text == 'Гаф':
            bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEMRXRmZLmnVnufYsOc7vFs6mCXVFkWkAACUQADrWW8FIai9pu49fluNQQ')
        elif message.text == 'Посмотреть калории':
            calories = users_data[chat_id].get('calories')
            bot.send_message(chat_id, f'Сегодня вы потратили {calories} калорий')
        elif message.text == 'Записать активность':
            inline = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton("Ходьба / Бег", callback_data="beg")
            button2 = types.InlineKeyboardButton("Пилон", callback_data="pil")
            button3 = types.InlineKeyboardButton("Метание ножей", callback_data="noz")
            inline.add(button1, button2, button3)
            bot.send_message(message.chat.id, "Выберите вид активности:", reply_markup=inline)
        elif message.text == 'Записать вес':
            set_weight(message)
        elif message.text == 'Записать рост':
            set_height(message)
        elif state == 'awaiting_weight':
            if message.text.replace('.', '', 1).isdigit():
                weight = float(message.text)
                if chat_id not in users_data:
                    users_data[chat_id] = {}
                users_data[chat_id]['weight'] = weight
                save_users_data(users_data)
                bot.send_message(chat_id, f"Ваш вес {weight} кг записан.")
                user_states[chat_id] = None
            else:
                bot.send_message(chat_id, 'Вес должен быть числом.')
        elif state == 'awaiting_height':
            if message.text.replace('.', '', 1).isdigit():
                height = float(message.text)
                if chat_id not in users_data:
                    users_data[chat_id] = {}
                users_data[chat_id]['height'] = height
                save_users_data(users_data)
                bot.send_message(chat_id, f"Ваш рост {height} см записан.")
                user_states[chat_id] = None
            else:
                bot.send_message(chat_id, 'Рост должен быть числом.')
        elif state == 'awaiting_distance':
            if message.text.replace('.', '', 1).isdigit():
                distance = float(message.text)
                if chat_id not in users_data:
                    users_data[chat_id] = {}
                users_data[chat_id]['distance'] = distance
                bot.send_message(chat_id, "Введите продолжительность прогулки в минутах:")
                user_states[chat_id] = 'awaiting_duration'
                print(f"User {chat_id} state set to awaiting_duration")  # Отладочное сообщение
            else:
                bot.send_message(chat_id, 'Расстояние должно быть числом.')
        elif state == 'awaiting_duration':
            if message.text.replace('.', '', 1).isdigit():
                try:
                    duration = int(message.text)
                    distance = users_data[chat_id].get('distance', 0)
                    m = users_data[chat_id].get('weight')
                    h = users_data[chat_id].get('height') / 100
                    v = distance * 1000 / (duration * 60)
                    calories = round((0.035 * m + ((v ** 2 / h) * 0.029 * m)) * duration)
                    if 'calories' not in users_data[chat_id]:
                        users_data[chat_id]['calories'] = 0
                    users_data[chat_id]['calories'] += calories
                    save_users_data(users_data)
                    bot.send_message(message.chat.id,
                                     f"Вы потратили {calories} калорий за {duration} минут прогулки на расстояние {distance} км. Всего потрачено калорий сегодня: {users_data[chat_id]['calories']}")
                    user_states[chat_id] = None
                except:
                    bot.send_message(message.chat.id, "Нет какой-то информации о Вас")
            else:
                bot.send_message(chat_id, 'Продолжительность должна быть числом.')
        elif state == 'awaiting_timepil':
            if message.text.replace('.', '', 1).isdigit():
                try:
                    timepil = int(message.text)
                    m = users_data[chat_id].get('weight')
                    calories = round(5.5*m*(timepil/60))
                    if 'calories' not in users_data[chat_id]:
                        users_data[chat_id]['calories'] = 0
                    users_data[chat_id]['calories'] += calories
                    save_users_data(users_data)
                    bot.send_message(message.chat.id,
                                     f"Вы потратили {calories} калорий за {timepil} минут тренировки. Всего потрачено калорий сегодня: {users_data[chat_id]['calories']}")
                    user_states[chat_id] = None
                except:
                    bot.send_message(message.chat.id, "Нет какой-то информации о Вас")
            else:
                bot.send_message(chat_id, 'Продолжительность должна быть числом.')
        elif state == 'awaiting_timenoz':
            if message.text.replace('.', '', 1).isdigit():
                try:
                    timenoz = int(message.text)
                    m = users_data[chat_id].get('weight')
                    calories = round(3.5*m*(timenoz/60))
                    if 'calories' not in users_data[chat_id]:
                        users_data[chat_id]['calories'] = 0
                    users_data[chat_id]['calories'] += calories
                    save_users_data(users_data)
                    bot.send_message(message.chat.id,
                                     f"Вы потратили {calories} калорий за {timenoz} минут тренировки. Всего потрачено калорий сегодня: {users_data[chat_id]['calories']}")
                    user_states[chat_id] = None
                except:
                    bot.send_message(message.chat.id, "Нет какой-то информации о Вас")
            else:
                bot.send_message(chat_id, 'Продолжительность должна быть числом.')
        else:
            bot.send_message(message.chat.id, 'Я такова не знаю, я глупенький')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = str(call.message.chat.id)
    if call.data == "beg":
        bot.send_message(call.message.chat.id, "Сколько километров прошли?")
        user_states[chat_id] = 'awaiting_distance'
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                              text='Ходьба / Бег')
    elif call.data == "pil":
        bot.send_message(call.message.chat.id, "Введите продолжительность тренировки в минутах:")
        user_states[chat_id] = 'awaiting_timepil'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Пилон')
    elif call.data == "noz":
        bot.send_message(call.message.chat.id, "Введите продолжительность тренировки в минутах:")
        user_states[chat_id] = 'awaiting_timenoz'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Метание ножей')


def scheduled_message():
    for user_id in ["1784266296"]:
        bot.send_message(user_id, "Федя тебя любит)")

def sceduled_time():
    for user_id in ["643651013"]:
        if user_id not in users_data:
            users_data[user_id] = {}
        users_data[user_id]['calories'] = float(0)
    save_users_data(users_data)

timezone = pytz.timezone('Europe/Samara')

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_message, CronTrigger(hour=15, minute=15, timezone=timezone))
scheduler.add_job(sceduled_time, CronTrigger(hour=0, minute=0, timezone=timezone))
scheduler.start()

if __name__ == '__main__':
    set_commands(bot)
    bot.polling(non_stop=True)