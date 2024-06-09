import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os

TOKEN = '7413652825:AAG8WrPJAmMgLpJdbltVgVn_3Tsr0lnn3TY'
bot = telebot.TeleBot(TOKEN)

USERS_FILE = r"C:\Users\herob\PycharmProjects\TeleBot\Telegram-Bot\Telegram Bot\users.json"  # Используем сырую строку

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

# Сохранение пользователей в файл
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    print(f"Users saved to {USERS_FILE}: {users}")

# Список пользователей
users = load_users()
print(f"Loaded users from {USERS_FILE}: {users}")

def set_commands(bot):
    commands = [
        types.BotCommand(command="/start", description="Главное меню"),
        types.BotCommand(command="/help", description="Получить помощь")
    ]
    bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def main(message):
    if message.chat.id not in users:
        users.append(message.chat.id)
        save_users(users)
        print(f"Added user {message.chat.id} to users list")

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Посчитать калории")
    button2 = types.KeyboardButton("Мур")

    menu.add(button1, button2)
    bot.send_message(message.chat.id, 'Ты солнышко (づ◔ ͜ʖ◔)づ', reply_markup=menu)

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Команды:\n/start - начать\n/help - помощь')

@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_message(message):
    if message.chat.type == 'private':
        if message.text == 'Мур':
            bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEMRXJmZLl1WE0gSfjnkYWJBzFEoVtvFQAC3wgAAvFVgVFsqsmMvkACrDUE')
        elif message.text == 'Посчитать калории':
            bot.send_message(message.chat.id, "Сколько киллометров прошла?")
        else:
            bot.send_message(message.chat.id, 'Я глупенький, я такова не знаю ((')

def scheduled_message():
    for user_id in [643016513, 643651013]:
        try:
            bot.send_message(user_id, "Ты самая красивая!")
        except:
            print("huy tam")


# Настройка планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_message, 'cron', hour=2, minute=1)  # Например, каждый день в 14:00
scheduler.start()
# Запуск бота и установка команд
if __name__ == '__main__':
    set_commands(bot)
    bot.polling(non_stop=True)