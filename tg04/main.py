import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

# УРОК

@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer(
        'Этот бот умеет выполнять команды:\n'
        '/start - основное меню задания tg04\n'
        '/help - список команд\n'
        '/links - ссылки на новости видео\n'
        '/dynamic - динамическое меню\n'
        '/start_lesson - меню из урока'
    )

@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)
    await callback.message.edit_text('Вот свежие новости!', reply_markup=await kb.test_keyboard())

@dp.message(F.text == "Тестовая кнопка 1")
async def test_button(message: Message):
    await message.answer('Обработка нажатия на reply кнопку')

# /start_lesson
@dp.message(Command('start_lesson'))
async def start_lesson_command(message: Message):
    await message.answer(
        f'Приветики, {message.from_user.first_name}',
        reply_markup=kb.inline_keyboard_test
    )

@dp.message(F.text == "Привет")
async def hello_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(F.text == "Пока")
async def bye_handler(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# ЗАДАНИЯ
# /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        f'Добро пожаловать, {message.from_user.first_name}! Выберите действие:',
        reply_markup=kb.greeting_keyboard
    )

# /links
@dp.message(Command("links"))
async def links_command(message: Message):
    await message.answer(
        "Новости видео:",
        reply_markup=kb.links_keyboard
    )

# /dynamic
@dp.message(Command("dynamic"))
async def dynamic_command(message: Message):
    await message.answer(
        "Нажмите кнопку для отображения дополнительных опций:",
        reply_markup=kb.initial_keyboard
    )

@dp.callback_query(F.data == "show_more")
async def show_more_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите категорию новостей видео:",
        reply_markup=kb.expanded_keyboard
    )
    await callback.answer()

@dp.callback_query(F.data == "foreign_video_news")
async def foreign_video_news_handler(callback: CallbackQuery):
    await callback.message.answer("Загружаю новости зарубежного видео...")
    await callback.answer()

@dp.callback_query(F.data == "russian_video_news")
async def russian_video_news_handler(callback: CallbackQuery):
    await callback.message.answer("Загружаю новости российского видео...")
    await callback.answer()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())