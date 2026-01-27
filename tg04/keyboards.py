from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

#УРОК
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Тестовая кнопка 1")],
        [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
    ],
    resize_keyboard=True
)

inline_keyboard_test = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Каталог", callback_data='catalog')],
        [InlineKeyboardButton(text="Новости", callback_data='news')],
        [InlineKeyboardButton(text="Профиль", callback_data='person')]
    ]
)

test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url='https://www.youtube.com/watch?v=HfaIcB4Ogxk'))
    return keyboard.adjust(2).as_markup()

# ЗАДАНИЯ
# Задание 1: Создание простого меню с кнопками
greeting_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True
)

# Задание 2: Кнопки с URL-ссылками
links_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новости зарубежного видео", url="https://www.kinopoisk.ru/media/news/")],
        [InlineKeyboardButton(text="Новости российского видео", url="https://www.film.ru/news")],
        [InlineKeyboardButton(text="Видеоновости кино", url="https://www.youtube.com/c/KinoNewsRu")]
    ]
)

# Задание 3: Динамическое изменение клавиатуры
initial_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ]
)

expanded_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новости зарубежного видео", callback_data="foreign_video_news")],
        [InlineKeyboardButton(text="Новости российского видео", callback_data="russian_video_news")]
    ]
)