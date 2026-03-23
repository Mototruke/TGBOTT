import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# Токен вашего бота
TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настройки yt-dlp
YDL_OPTIONS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'noplaylist': True,
}

async def download_video(url: str):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Пришли мне ссылку на видео из Rutube или VK, и я попробую его скачать.")

@dp.message(F.text.contains("rutube.ru") | F.text.contains("://vk.com"))
async def handle_video(message: types.Message):
    status_msg = await message.answer("Начинаю загрузку... Подождите.")
    url = message.text
    
    try:
        # Запуск скачивания в отдельном потоке, чтобы не блокировать бота
        file_path = await asyncio.to_thread(download_video, url)
        
        # Отправка видео
        video = types.FSInputFile(file_path)
        await message.answer_video(video, caption="Ваше видео готово!")
        
        # Удаляем файл после отправки
        os.remove(file_path)
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"Ошибка при скачивании: {e}")

async def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
