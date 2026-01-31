import asyncio
import random
import requests
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Импортируем конфигурационные данные
from config import TOKEN, NASA_API_KEY

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_random_apod():
    # Текущая дата (сегодня)
    end_date = datetime.now()
    
    # Дата год назад (начало диапазона)
    start_date = end_date - timedelta(days=365)
    
    # Генерируем случайную дату между start_date и end_date
    random_date = start_date + (end_date - start_date) * random.random()
    
    # Форматируем дату в строку (YYYY-MM-DD)
    date_str = random_date.strftime("%Y-%m-%d")
    
    # Формируем URL для запроса к NASA API
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
    
    # Отправляем GET-запрос
    response = requests.get(url)
    
    # Возвращаем ответ в формате JSON
    return response.json()

@dp.message(Command("start"))
async def start_command(message: Message):
    welcome_text = (
        "Добро пожаловать в NASA Cosmic Explorer! \n\n"
        "Я покажу вам удивительные космические снимки!\n\n"
        "Доступные команды:\n"
        "/random_apod - случайное космическое фото дня\n"
        "/help - справка по командам"
    )
    await message.answer(welcome_text)

@dp.message(Command("help"))
async def help_command(message: Message):
    """
    Обработчик команды /help
    """
    help_text = (
        "Справка по командам:\n\n"
        "/random_apod - Получить случайное космическое изображение дня\n"
        "NASA Astronomy Picture of the Day (APOD) - это ежедневные снимки\n"
        "космоса с пояснениями от профессиональных астрономов.\n\n"
        "Каждое изображение уникально и показывает красоту нашей Вселенной!"
    )
    await message.answer(help_text)

@dp.message(Command("random_apod"))
async def random_apod(message: Message):
    # Информируем пользователя о начале загрузки
    await message.answer("🛰 Загружаю космическое изображение...")
    
    # Получаем данные о случайном APOD
    apod_data = get_random_apod()
    
    # Проверяем, что запрос выполнен успешно
    if 'url' in apod_data:
        # Извлекаем URL изображения и заголовок
        photo_url = apod_data['url']
        title = apod_data.get('title', 'Без названия')
        
        # Формируем подпись с дополнительной информацией
        caption = (
            f" **{title}**\n\n"
            f" Дата: {apod_data.get('date', 'Не указана')}\n"
            f" Автор: {apod_data.get('copyright', 'NASA')}"
        )
        
        # Добавляем описание, если оно есть
        if 'explanation' in apod_data:
            # Обрезаем длинное описание для Telegram
            explanation = apod_data['explanation']
            if len(explanation) > 500:
                explanation = explanation[:500] + "..."
            caption += f"\n\n📝 {explanation}"
        
        # Отправляем изображение с подписью
        await message.answer_photo(photo=photo_url, caption=caption)
    else:
        # Если произошла ошибка
        error_text = (
            "❌ Не удалось загрузить изображение.\n"
            "Возможные причины:\n"
            "• Проблемы с подключением к интернету\n"
            "• Ошибка API NASA\n"
            "• На выбранную дату нет изображения"
        )
        await message.answer(error_text)

@dp.message()
async def handle_other_messages(message: Message):
    """
    Обработчик всех остальных сообщений
    """
    await message.answer(
        "Используйте команды для взаимодействия с ботом:\n"
        "/start - начать работу\n"
        "/random_apod - получить космическое изображение\n"
        "/help - справка"
    )

async def main():
    print("NASA бот запущен! Ожидаю команды...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())