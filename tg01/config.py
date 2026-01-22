"""
Файл конфигурации для хранения констант и настроек бота.
"""
import os

# Загружаем переменные окружения из .env файла
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ Предупреждение: python-dotenv не установлен. Установите: pip install python-dotenv")

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверяем, что токен получен
if not BOT_TOKEN:
    raise ValueError(
        "❌ Токен бота не найден!\n"
        "Создайте файл .env в папке проекта и добавьте:\n"
        "BOT_TOKEN=ваш_токен_здесь\n\n"
        "Получить токен можно у @BotFather в Telegram"
    )

# Конфигурация для API погоды
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
# Координаты для Москвы
LATITUDE = 55.7558
LONGITUDE = 37.6173