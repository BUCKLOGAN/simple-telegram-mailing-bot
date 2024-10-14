import telebot
from telebot.types import Message
import os
from config import TOKEN, ADMIN_ID, USERS_FILE

bot = telebot.TeleBot(TOKEN)

def save_user_id(user_id):
    with open(USERS_FILE, 'a+') as file:
        file.seek(0)
        if str(user_id) not in file.read().splitlines():
            file.write(f"{user_id}\n")

@bot.message_handler(commands=['start'])
def start(message: Message):
    user_id = message.from_user.id
    save_user_id(user_id)
    bot.reply_to(message, "❤Вы подписались на рассылку")

@bot.message_handler(commands=['send'])
def send_broadcast(message: Message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return

    bot.reply_to(message, "Введите текст для рассылки:")
    bot.register_next_step_handler(message, process_broadcast_text)

def process_broadcast_text(message: Message):
    broadcast_text = message.text
    
    if not os.path.exists(USERS_FILE):
        bot.reply_to(message, "Файл с пользователями не найден.")
        return

    with open(USERS_FILE, 'r') as file:
        user_ids = file.read().splitlines()

    successful = 0
    failed = 0

    for user_id in user_ids:
        try:
            bot.send_message(int(user_id), broadcast_text)
            successful += 1
        except Exception:
            failed += 1

    stats = f"Рассылка завершена.\nУспешно отправлено: {successful}\nНе удалось отправить: {failed}"
    bot.reply_to(message, stats)

bot.polling()