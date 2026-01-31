import asyncio
import requests
import random
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN, KINOPOISK_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def search_movie_by_name(movie_name):
    url = f"https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={movie_name}&page=1"
    headers = {
        "X-API-KEY": KINOPOISK_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('films'):
                return data['films'][0]
        return None
    except:
        return None

def get_popular_movies():
    url = "https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_100_POPULAR_FILMS&page=1"
    headers = {
        "X-API-KEY": KINOPOISK_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('films'):
                return data['films']
        return []
    except:
        return []

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Команды бота:\n"
        "/search [название] - поиск фильма\n"
        "/random - случайный популярный фильм\n"
        "/help - справка"
    )

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Этот бот ищет информацию о фильмах.\n\n"
        "Примеры использования:\n"
        "/search Интерстеллар\n"
        "/random\n"
        "Или просто напишите название фильма"
    )

@dp.message(Command("search"))
async def search_command(message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Укажите название фильма: /search [название]")
        return
    
    movie_name = " ".join(args[1:])
    movie_info = search_movie_by_name(movie_name)
    
    if movie_info:
        title = movie_info.get('nameRu', 'Без названия')
        year = movie_info.get('year', 'Неизвестен')
        rating = movie_info.get('rating', 'Нет')
        
        info = f"{title}\nГод: {year}\nРейтинг: {rating}"
        
        poster_url = movie_info.get('posterUrl')
        if poster_url and poster_url.startswith('http'):
            await message.answer_photo(photo=poster_url, caption=info)
        else:
            await message.answer(info)
    else:
        await message.answer(f"Фильм '{movie_name}' не найден.")

@dp.message(Command("random"))
async def random_command(message: Message):
    movies = get_popular_movies()
    
    if movies:
        movie = random.choice(movies)
        title = movie.get('nameRu', 'Без названия')
        year = movie.get('year', 'Неизвестен')
        rating = movie.get('rating', 'Нет')
        
        info = f"Случайный популярный фильм:\n\n{title}\nГод: {year}\nРейтинг: {rating}"
        
        poster_url = movie.get('posterUrl')
        if poster_url and poster_url.startswith('http'):
            await message.answer_photo(photo=poster_url, caption=info)
        else:
            await message.answer(info)
    else:
        await message.answer("Не удалось получить список фильмов.")

# Обработчик текстовых сообщений (если пользователь просто пишет название)
@dp.message()
async def handle_text(message: Message):
    # Если сообщение начинается с /, это команда - пропускаем
    if message.text.startswith('/'):
        return
    
    movie_name = message.text.strip()
    
    if not movie_name:
        await message.answer("Введите название фильма.")
        return
    
    movie_info = search_movie_by_name(movie_name)
    
    if movie_info:
        title = movie_info.get('nameRu', 'Без названия')
        year = movie_info.get('year', 'Неизвестен')
        rating = movie_info.get('rating', 'Нет')
        
        info = f"{title}\nГод: {year}\nРейтинг: {rating}"
        
        poster_url = movie_info.get('posterUrl')
        if poster_url and poster_url.startswith('http'):
            await message.answer_photo(photo=poster_url, caption=info)
        else:
            await message.answer(info)
    else:
        await message.answer(f"Фильм '{movie_name}' не найден.")

async def set_bot_commands():
    from aiogram.types import BotCommand
    
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="search", description="Поиск фильма"),
        BotCommand(command="random", description="Случайный фильм"),
        BotCommand(command="help", description="Справка")
    ]
    
    await bot.set_my_commands(commands)

async def main():
    await set_bot_commands()
    print("Бот запущен с меню команд")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())