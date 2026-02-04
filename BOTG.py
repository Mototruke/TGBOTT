import telebot
from telebot import types
import yt_dlp
import os
bot = telebot.TeleBot('8201401291:AAF_Aj_y74xXJ9ZTwO2-2lQ_-DEi376NDvU')
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id,
                     "👋 Привет! Я твой бот-помощник!\n\nПросто пришли мне ссылку на YouTube видео, и я его скачаю.",
                     reply_markup=markup)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton
        btn2 = types.KeyboardButton
        btn3 = types.KeyboardButton
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, 'Чтобы скачать видео, просто отправьте мне ссылку!')
        bot.send_message(message.from_user.id, 'Если видео слишком длинное, Telegram может его не пропустить.')
    elif "youtube.com" in message.text or "youtu.be" in message.text:
        url = message.text
        msg = bot.send_message(message.chat.id, "⏳ Начинаю загрузку... Пожалуйста, подождите.")
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': '%(title)s.%(ext)s',
                'max_filesize': 50000000,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
            with open(file_path, 'rb') as video:
                bot.send_video(message.chat.id, video, caption=f"✅ Готово: {info.get('title')}")
            os.remove(file_path)
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Ошибка при скачивании: {str(e)}", message.chat.id, msg.message_id)
bot.polling(none_stop=True, interval=0)