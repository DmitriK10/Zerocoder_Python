import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кэш для списка пород
_breeds_cache = None

def get_cat_breeds():
    """Получение списка пород кошек"""
    global _breeds_cache
    
    # Используем кэш, если данные уже загружены
    if _breeds_cache is not None:
        return _breeds_cache
    
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}
    
    try:
        # Увеличиваем таймаут до 30 секунд
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            breeds = response.json()
            _breeds_cache = breeds  # Сохраняем в кэш
            return breeds
        else:
            print(f"Ошибка API: {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        print("Таймаут при загрузке списка пород")
        return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def get_cat_image_by_breed(breed_id):
    """Получение изображения кошки по ID породы"""
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    
    try:
        # Увеличиваем таймаут
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0]['url']
        
        # Если нет изображения для породы, возвращаем случайное
        return "https://cdn2.thecatapi.com/images/0XYvRd7oD.jpg"
    except requests.exceptions.Timeout:
        print("Таймаут при загрузке изображения")
        return "https://cdn2.thecatapi.com/images/0XYvRd7oD.jpg"
    except Exception as e:
        print(f"Ошибка: {e}")
        return "https://cdn2.thecatapi.com/images/0XYvRd7oD.jpg"

def get_breed_info(breed_name):
    """Поиск информации о породе"""
    breeds = get_cat_breeds()
    
    if not breeds:
        return None
    
    # Приводим к нижнему регистру для сравнения
    breed_name_lower = breed_name.lower()
    
    # Сначала ищем точное совпадение
    for breed in breeds:
        if breed['name'].lower() == breed_name_lower:
            return breed
    
    # Затем ищем частичное совпадение
    for breed in breeds:
        if breed_name_lower in breed['name'].lower():
            return breed
    
    return None

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Напиши мне название породы кошки на английском, "
        "и я пришлю тебе её фото и описание."
    )

@dp.message()
async def send_cat_info(message: Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    
    if breed_info:
        # Показываем, что бот работает
        await message.answer(f"Найдена порода: {breed_info['name']}")
        
        # Получаем изображение
        cat_image_url = get_cat_image_by_breed(breed_info['id'])
        
        # Формируем информацию
        info = (
            f"Порода: {breed_info['name']}\n"
            f"Происхождение: {breed_info.get('origin', 'Неизвестно')}\n"
            f"Описание: {breed_info.get('description', 'Нет описания')[:150]}...\n"
            f"Характер: {breed_info.get('temperament', 'Не указан')}\n"
            f"Продолжительность жизни: {breed_info.get('life_span', 'Неизвестно')} лет"
        )
        
        # Отправляем фото и информацию
        await message.answer_photo(photo=cat_image_url, caption=info)
    else:
        # Предлагаем популярные породы
        popular = ["Siamese", "Persian", "Maine Coon", "Bengal", "Ragdoll"]
        await message.answer(
            f"Порода '{breed_name}' не найдена.\n\n"
            f"Попробуйте одну из этих:\n" + "\n".join(popular)
        )

async def main():
    print("Бот с кошками запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())