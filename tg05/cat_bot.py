import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Импортируем конфигурационные данные
from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_cat_breeds():
    # URL для получения списка пород
    url = "https://api.thecatapi.com/v1/breeds"
    
    # Заголовки с API-ключом (требуется для аутентификации)
    headers = {"x-api-key": THE_CAT_API_KEY}
    
    # Отправляем GET-запрос к API
    response = requests.get(url, headers=headers)
    
    # Возвращаем ответ в формате JSON
    return response.json()

def get_cat_image_by_breed(breed_id):
    # Формируем URL с параметром breed_id
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    
    # Заголовки с API-ключом
    headers = {"x-api-key": THE_CAT_API_KEY}
    
    # Отправляем запрос и получаем данные
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Извлекаем URL изображения из ответа
    return data[0]['url']

def get_breed_info(breed_name):
    # Получаем список всех пород
    breeds = get_cat_breeds()
    
    # Ищем породу по названию (без учета регистра)
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    
    # Если порода не найдена, возвращаем None
    return None

@dp.message(Command("start"))
async def start_command(message: Message):

    welcome_text = (
        "Привет! Я бот-знаток кошачьих пород! \n\n"
        "Напиши мне название породы кошки, и я пришлю тебе:\n"
        "• Фото котика этой породы\n"
        "• Подробное описание породы\n\n"
        "Например: 'Siamese', 'Persian', 'Maine Coon'"
    )
    await message.answer(welcome_text)

@dp.message()
async def send_cat_info(message: Message):
    # Получаем название породы из сообщения пользователя
    breed_name = message.text
    
    # Ищем информацию о породе
    breed_info = get_breed_info(breed_name)
    
    if breed_info:
        # Если порода найдена, получаем URL изображения
        cat_image_url = get_cat_image_by_breed(breed_info['id'])
        
        # Формируем информационное сообщение
        info = (
            f" **Порода:** {breed_info['name']}\n"
            f" **Происхождение:** {breed_info.get('origin', 'Не указано')}\n"
            f" **Описание:** {breed_info.get('description', 'Описание отсутствует')}\n"
            f" **Характер:** {breed_info.get('temperament', 'Не указан')}\n"
            f" **Продолжительность жизни:** {breed_info.get('life_span', 'Не указана')} лет"
        )
        
        # Отправляем фото с подписью
        await message.answer_photo(photo=cat_image_url, caption=info)
    else:
        # Если порода не найдена
        error_text = (
            "К сожалению, порода не найдена. \n\n"
            "Проверьте правильность написания или попробуйте другую породу.\n"
            "Примеры доступных пород:\n"
            "• Siamese (Сиамская)\n"
            "• Persian (Персидская)\n"
            "• Maine Coon (Мейн-кун)\n"
            "• Bengal (Бенгальская)"
        )
        await message.answer(error_text)

async def main():
    print("Бот запущен! Ожидаю сообщений...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())