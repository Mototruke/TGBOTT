import telebot
from telebot import types
import yt_dlp
import os
bot = telebot.TeleBot('')
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     "Привет! Я твой бот-помощник!\n\nПросто пришли мне ссылку на YouTube, и я скачаю видео.",
                     reply_markup=markup)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Поздороваться":
        bot.send_message(message.chat.id, "Привет! Чтобы скачать видео, просто отправьте мне ссылку!")
        bot.send_message(message.chat.id, "Учти, что Telegram не принимает файлы больше 50 МБ (через обычных ботов).")

    elif "youtube.com" in message.text or "youtu.be" in message.text:
        url = message.text
        msg = bot.send_message(message.chat.id, "Начинаю загрузку... Пожалуйста, подождите.")
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': 'video_%(id)s.%(ext)s',
                'max_filesize': 50000000,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
            with open(file_path, 'rb') as video:
                bot.send_video(message.chat.id, video, caption=f"Готово: {info.get('title')}")
            os.remove(file_path)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"Ошибка: {str(e)}", message.chat.id, msg.message_id)
bot.polling(none_stop=True)
