import aiohttp
import urllib.parse
from config import WEATHER_API_URL, LATITUDE, LONGITUDE


async def get_weather() -> str:
    """
    Получение погоды
    """
    try:
        # Правильно формируем параметры
        params = {
            "latitude": str(LATITUDE),    # Преобразуем в строку
            "longitude": str(LONGITUDE),  # Преобразуем в строку
            "current_weather": "true",    # Только строка!
            "timezone": "auto"
        }
        
        # Формируем URL с параметрами вручную
        query_string = urllib.parse.urlencode(params)
        url = f"{WEATHER_API_URL}?{query_string}"
        
        print(f"📡 Запрос к: {url}")  # Для отладки
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data.get("current_weather", {})
                    
                    temp = current.get("temperature", "N/A")

                    weather_code = current.get("weathercode", 0)
                    if weather_code in [0, 1]:
                        description = "Ясно ☀️"
                    elif weather_code in [2, 3]:
                        description = "Облачно ☁️"
                    elif weather_code in [45, 48]:
                        description = "Туман 🌫️"
                    elif weather_code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67]:
                        description = "Дождь 🌧️"
                    elif weather_code in [71, 73, 75, 77, 85, 86]:
                        description = "Снег ❄️"
                    elif weather_code in [95, 96, 99]:
                        description = "Гроза ⛈️"
                    else:
                        description = "Разнообразно 🌈"
                    
                    return f"🌤️ Погода в Москве: {temp}°C, {description}"
                else:
                    error_text = await response.text()
                    print(f"❌ Ошибка API: {error_text}")
                    return "❌ Не удалось получить данные о погоде"
                    
    except aiohttp.ClientError as e:
        print(f"🌐 Ошибка сети: {e}")
        return "⚠️ Ошибка подключения к сервису погоды. Проверьте интернет-соединение."
    except Exception as e:
        print(f"⚠️ Неожиданная ошибка: {e}")
        return "⚠️ Ошибка подключения к сервису погоды"