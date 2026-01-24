import os
import random
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Импорт библиотек aiogram
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile

# Импорт для работы с озвучкой и переводом
from gtts import gTTS
from googletrans import Translator

# Загрузка переменных окружения
load_dotenv()

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Проверка наличия токена
if not BOT_TOKEN:
    print("ОШИБКА: Не найден BOT_TOKEN в переменных окружения")
    print("Создайте файл .env и добавьте: BOT_TOKEN='ваш_токен_бота'")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = Translator()

# Создание необходимых папок
Path("img").mkdir(exist_ok=True)
Path("tmp").mkdir(exist_ok=True)
Path("media").mkdir(exist_ok=True)

# ============================================================================
# 1. ОБРАБОТЧИКИ КОМАНД
# ============================================================================

@dp.message(CommandStart())
async def handle_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(f"Привет, {message.from_user.first_name}! Я бот для работы с мультимедиа.")

@dp.message(Command("help"))
async def handle_help(message: Message):
    """Обработчик команды /help"""
    help_text = """Доступные команды:

/start - Начать диалог
/help - Показать это сообщение
/photo - Получить фотографию
/video - Получить видео файл
/audio - Получить аудио файл
/voice - Получить голосовое сообщение
/doc - Получить документ PDF
/training - Получить мини-тренировку

Особенности бота:
1. Сохраняет все полученные фото в папку /img
2. Отвечает на любой текст переводом на английский
3. Отправляет голосовые сообщения"""
    await message.answer(help_text)

@dp.message(Command("photo"))
async def send_photo(message: Message):
    """Отправка фото пользователю"""
    try:
        photo_path = "media/sample_photo.jpg"
        
        if os.path.exists(photo_path):
            photo = FSInputFile(photo_path)
            await bot.send_photo(message.chat.id, photo, caption="Вот ваше фото")
        else:
            await message.answer("Фото не найдено. Вы можете отправить мне фото - я сохраню его.")
    except Exception as e:
        await message.answer(f"Ошибка при отправке фото: {e}")

@dp.message(Command("video"))
async def send_video(message: Message):
    """Отправка видео файла"""
    try:
        await bot.send_chat_action(message.chat.id, "upload_video")
        
        video_path = "media/video.mp4"
        
        if os.path.exists(video_path):
            video = FSInputFile(video_path)
            await bot.send_video(message.chat.id, video, caption="Вот видео файл")
        else:
            await message.answer("Видео файл не найден. Создайте файл media/video.mp4")
    except Exception as e:
        await message.answer(f"Ошибка при отправке видео: {e}")

@dp.message(Command("audio"))
async def send_audio(message: Message):
    """Отправка аудио файла"""
    try:
        audio_path = "media/sound2.mp3"
        
        if os.path.exists(audio_path):
            audio = FSInputFile(audio_path)
            await bot.send_audio(message.chat.id, audio, title="Пример аудио", performer="Bot")
        else:
            await message.answer("Аудио файл не найден. Создайте файл media/sound2.mp3")
    except Exception as e:
        await message.answer(f"Ошибка при отправке аудио: {e}")

@dp.message(Command("voice"))
async def send_voice(message: Message):
    """Отправка голосового сообщения"""
    try:
        voice_path = "media/sample.ogg"
        
        if os.path.exists(voice_path):
            voice = FSInputFile(voice_path)
            await bot.send_voice(message.chat.id, voice)
        else:
            await message.answer("Голосовое сообщение не найдено. Используйте /training для генерации голосового сообщения")
    except Exception as e:
        await message.answer(f"Ошибка при отправке голосового сообщения: {e}")

@dp.message(Command("doc"))
async def send_document(message: Message):
    """Отправка PDF документа"""
    try:
        doc_path = "media/TG02.pdf"
        
        if os.path.exists(doc_path):
            document = FSInputFile(doc_path)
            await bot.send_document(message.chat.id, document, caption="PDF документ")
        else:
            await message.answer("Документ не найден. Создайте файл media/TG02.pdf")
    except Exception as e:
        await message.answer(f"Ошибка при отправке документа: {e}")

@dp.message(Command("training"))
async def send_training(message: Message):
    """Отправка мини-тренировки с озвучкой"""
    try:
        training_list = [
            "Тренировка 1: 1. Скручивания: 3 подхода по 15 повторений. 2. Велосипед: 3 подхода по 20 повторений. 3. Планка: 3 подхода по 30 секунд",
            "Тренировка 2: 1. Подъемы ног: 3 подхода по 15 повторений. 2. Русский твист: 3 подхода по 20 повторений. 3. Планка с поднятой ногой: 3 подхода по 20 секунд",
            "Тренировка 3: 1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений. 2. Горизонтальные ножницы: 3 подхода по 20 повторений. 3. Боковая планка: 3 подхода по 20 секунд"
        ]
        
        random_training = random.choice(training_list)
        training_text = f"Ваша мини-тренировка на сегодня: {random_training}"
        
        await message.answer(training_text)
        
        tts = gTTS(text=random_training, lang='ru')
        audio_filename = f"tmp/training_{message.chat.id}.ogg"
        tts.save(audio_filename)
        
        voice = FSInputFile(audio_filename)
        await bot.send_voice(message.chat.id, voice)
        
        os.remove(audio_filename)
        
    except Exception as e:
        await message.answer(f"Ошибка при создании тренировки: {e}")

# ============================================================================
# 2. ОБРАБОТЧИКИ СООБЩЕНИЙ ПО ТИПУ КОНТЕНТА
# ============================================================================

@dp.message(F.photo)
async def handle_photo(message: Message):
    """Обработка фото от пользователя - сохраняет все фото в папку /img"""
    try:
        photo = message.photo[-1]
        file_id = photo.file_id
        
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        timestamp = int(message.date.timestamp())
        filename = f"img/photo_{message.from_user.id}_{timestamp}.jpg"
        
        await bot.download_file(file_path, filename)
        
        await message.answer(f"Фото сохранено в папку /img. Имя файла: {os.path.basename(filename)}")
        
    except Exception as e:
        await message.answer(f"Ошибка при сохранении фото: {e}")

# ============================================================================
# 3. УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ
# ============================================================================

@dp.message(F.text)
async def handle_text(message: Message):
    """Обработка текстовых сообщений - переводит любой текст на английский язык"""
    user_text = message.text.strip()
    
    if user_text.startswith('/'):
        return
    
    try:
        translation = translator.translate(user_text, src='ru', dest='en')
        
        response = f"Оригинал: {user_text}\n"
        response += f"Перевод: {translation.text}"
        
        await message.answer(response)
        
    except Exception as e:
        await message.answer(f"Не удалось перевести текст. Ошибка: {e}")

# ============================================================================
# 4. ОБРАБОТКА ДРУГИХ ТИПОВ СООБЩЕНИЙ
# ============================================================================

@dp.message(F.voice)
async def handle_voice(message: Message):
    """Обработка голосовых сообщений от пользователя"""
    await message.answer("Получил ваше голосовое сообщение.")

@dp.message(F.document)
async def handle_document(message: Message):
    """Обработка документов от пользователя"""
    await message.answer("Получил ваш документ.")

# ============================================================================
# 5. ЗАПУСК БОТА
# ============================================================================

async def main():
    """Основная функция запуска бота"""
    print("Бот запускается...")
    print(f"Папка проекта: {os.getcwd()}")
    print(f"Созданные папки: img/, tmp/, media/")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    required_folders = ['img', 'tmp', 'media']
    for folder in required_folders:
        os.makedirs(folder, exist_ok=True)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")