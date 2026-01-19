#!/usr/bin/env python3
"""
Telegram Bot для интеграции с Django API

Этот бот выступает в роли клиента, который отправляет запросы
к Django REST API для регистрации пользователей и получения информации.
"""

import telebot
from telebot import types
import requests
import json
import logging
from datetime import datetime

# ==================== КОНФИГУРАЦИЯ ====================
API_URL = "http://127.0.0.1:8000/api"  # URL Django API
BOT_TOKEN = "8115874316:AAFw5uLmk522qmnOIGrLPe8WCKvZ4HrzXOQ"     # Токен бота от @BotFather

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def send_api_request(endpoint, method='GET', data=None):
    """
    Отправка запроса к Django API.
    
    Args:
        endpoint (str): Конечная точка API
        method (str): HTTP метод (GET, POST, DELETE)
        data (dict): Данные для отправки
    
    Returns:
        dict: Ответ от API
    """
    url = f"{API_URL}/{endpoint.lstrip('/')}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=10)
        elif method.upper() == 'POST':
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, timeout=10)
        else:
            return {'error': f'Неизвестный метод: {method}'}
        
        # Логирование запроса
        logger.info(f"API Request: {method} {url} - Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            return {
                'success': True,
                'data': response.json(),
                'status_code': response.status_code
            }
        else:
            return {
                'success': False,
                'error': f'API вернул статус {response.status_code}',
                'details': response.text,
                'status_code': response.status_code
            }
            
    except requests.exceptions.ConnectionError:
        logger.error(f"Не удалось подключиться к API: {url}")
        return {
            'success': False,
            'error': 'Не удалось подключиться к серверу API'
        }
    except requests.exceptions.Timeout:
        logger.error(f"Таймаут при подключении к API: {url}")
        return {
            'success': False,
            'error': 'Таймаут при подключении к серверу'
        }
    except Exception as e:
        logger.error(f"Ошибка при запросе к API: {str(e)}")
        return {
            'success': False,
            'error': f'Ошибка при запросе к API: {str(e)}'
        }

def format_user_info(user_data):
    """
    Форматирование информации о пользователе для отправки в Telegram.
    
    Args:
        user_data (dict): Данные пользователя
    
    Returns:
        str: Отформатированная строка с информацией
    """
    username = user_data.get('username', 'не указан')
    first_name = user_data.get('first_name', 'не указано')
    last_name = user_data.get('last_name', 'не указано')
    created_at = user_data.get('created_at', 'неизвестно')
    
    # Форматирование даты
    if created_at != 'неизвестно':
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            created_at = dt.strftime("%d.%m.%Y %H:%M:%S")
        except:
            pass
    
    return (
        f"👤 <b>Информация о пользователе:</b>\n\n"
        f"🆔 <b>ID:</b> {user_data.get('user_id', 'N/A')}\n"
        f"📛 <b>Username:</b> @{username if username else 'нет'}\n"
        f"👨 <b>Имя:</b> {first_name}\n"
        f"👨‍🦳 <b>Фамилия:</b> {last_name}\n"
        f"📅 <b>Дата регистрации:</b> {created_at}\n"
        f"🔄 <b>Последняя активность:</b> {user_data.get('last_activity', 'неизвестно')}\n"
        f"✅ <b>Статус:</b> {'Активен' if user_data.get('is_active') else 'Неактивен'}"
    )

# ==================== ОБРАБОТЧИКИ КОМАНД ====================

@bot.message_handler(commands=['start'])
def handle_start(message):
    """
    Обработчик команды /start.
    
    Регистрирует пользователя в системе через Django API
    и отправляет приветственное сообщение.
    """
    user = message.from_user
    chat_id = message.chat.id
    
    logger.info(f"Команда /start от пользователя {user.id} ({user.username})")
    
    # Отправка сообщения о начале регистрации
    bot.send_chat_action(chat_id, 'typing')
    bot.send_message(
        chat_id,
        "🔄 <b>Регистрация в системе...</b>\n"
        "Пожалуйста, подождите немного."
    )
    
    # Подготовка данных для API
    user_data = {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    
    # Отправка запроса к Django API
    response = send_api_request('register/', 'POST', user_data)
    
    # Обработка ответа от API
    if response['success']:
        api_data = response['data']
        
        if response['status_code'] == 201:
            # Пользователь успешно зарегистрирован
            bot.send_message(
                chat_id,
                "✅ <b>Регистрация успешно завершена!</b>\n\n"
                f"Добро пожаловать, {user.first_name or 'пользователь'}!\n"
                "Теперь вы зарегистрированы в нашей системе.\n\n"
                "Доступные команды:\n"
                "/myinfo - ваша информация\n"
                "/help - справка по командам"
            )
            
            # Логирование успешной регистрации
            logger.info(f"Пользователь {user.id} успешно зарегистрирован")
            
        elif response['status_code'] == 200:
            # Пользователь уже был зарегистрирован
            bot.send_message(
                chat_id,
                "ℹ️ <b>Вы уже зарегистрированы в системе!</b>\n\n"
                "Ваши данные были обновлены.\n"
                "Используйте /myinfo для просмотра вашей информации."
            )
            
            logger.info(f"Данные пользователя {user.id} обновлены")
    else:
        # Ошибка при регистрации
        error_msg = response.get('error', 'Неизвестная ошибка')
        bot.send_message(
            chat_id,
            f"❌ <b>Ошибка при регистрации!</b>\n\n"
            f"Причина: {error_msg}\n"
            "Попробуйте позже или обратитесь к администратору."
        )
        
        logger.error(f"Ошибка регистрации пользователя {user.id}: {error_msg}")

@bot.message_handler(commands=['myinfo'])
def handle_myinfo(message):
    """
    Обработчик команды /myinfo.
    
    Получает информацию о пользователе из Django API
    и отправляет ее в Telegram.
    """
    user = message.from_user
    chat_id = message.chat.id
    
    logger.info(f"Команда /myinfo от пользователя {user.id}")
    
    # Отправка сообщения о загрузке
    bot.send_chat_action(chat_id, 'typing')
    bot.send_message(
        chat_id,
        "📊 <b>Получение информации...</b>\n"
        "Запрашиваю ваши данные из системы."
    )
    
    # Отправка запроса к Django API
    response = send_api_request(f'user/{user.id}/', 'GET')
    
    # Обработка ответа от API
    if response['success']:
        api_data = response['data']
        
        if api_data.get('status') == 'success':
            # Успешно получена информация
            user_info = format_user_info(api_data['data'])
            bot.send_message(chat_id, user_info)
            
            logger.info(f"Информация о пользователе {user.id} успешно получена")
        else:
            # Пользователь не найден
            bot.send_message(
                chat_id,
                "⚠️ <b>Вы не зарегистрированы в системе!</b>\n\n"
                "Используйте команду /start для регистрации."
            )
            
            logger.warning(f"Пользователь {user.id} не найден в системе")
    else:
        # Ошибка при получении информации
        error_msg = response.get('error', 'Неизвестная ошибка')
        bot.send_message(
            chat_id,
            f"❌ <b>Ошибка при получении информации!</b>\n\n"
            f"Причина: {error_msg}\n"
            "Попробуйте позже или обратитесь к администратору."
        )
        
        logger.error(f"Ошибка получения информации о пользователе {user.id}: {error_msg}")

@bot.message_handler(commands=['help'])
def handle_help(message):
    """
    Обработчик команды /help.
    
    Отправляет справку по доступным командам.
    """
    help_text = (
        "🤖 <b>Telegram Bot - Справка по командам</b>\n\n"
        
        "👋 <b>Основные команды:</b>\n"
        "/start - Регистрация в системе\n"
        "/myinfo - Ваша информация в системе\n"
        "/help - Эта справка\n\n"
        
        "📊 <b>Информация:</b>\n"
        "Этот бот интегрирован с Django REST API.\n"
        "При регистрации ваши данные сохраняются в базе данных.\n\n"
        
        "🔧 <b>Техническая информация:</b>\n"
        f"API URL: {API_URL}\n"
        "Для получения токена бота обратитесь к @BotFather\n\n"
        
        "⚠️ <b>Примечание:</b>\n"
        "Бот не хранит ваши личные данные локально.\n"
        "Все данные обрабатываются через защищенное API."
    )
    
    bot.send_message(message.chat.id, help_text)
    
    logger.info(f"Команда /help от пользователя {message.from_user.id}")

@bot.message_handler(commands=['users'])
def handle_users(message):
    """
    Обработчик команды /users (только для администраторов).
    
    Получает список всех зарегистрированных пользователей.
    """
    user = message.from_user
    
    # Проверка прав администратора (можно настроить по user_id)
    ADMIN_IDS = [123456789]  # Замените на реальные ID администраторов
    
    if user.id not in ADMIN_IDS:
        bot.send_message(
            message.chat.id,
            "⛔ <b>Доступ запрещен!</b>\n\n"
            "Эта команда доступна только администраторам."
        )
        return
    
    logger.info(f"Команда /users от администратора {user.id}")
    
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id,
        "📋 <b>Получение списка пользователей...</b>"
    )
    
    # Отправка запроса к Django API
    response = send_api_request('users/', 'GET')
    
    if response['success']:
        api_data = response['data']
        
        if api_data.get('status') == 'success':
            users = api_data['data']
            count = api_data.get('count', 0)
            
            if count > 0:
                users_list = []
                for i, user_data in enumerate(users[:10], 1):  # Ограничиваем 10 пользователями
                    username = user_data.get('username', 'нет')
                    user_id = user_data.get('user_id', 'N/A')
                    users_list.append(f"{i}. @{username} (ID: {user_id})")
                
                users_text = "\n".join(users_list)
                
                if count > 10:
                    users_text += f"\n\n... и еще {count - 10} пользователей"
                
                bot.send_message(
                    message.chat.id,
                    f"👥 <b>Зарегистрированные пользователи:</b>\n\n"
                    f"Всего пользователей: {count}\n\n"
                    f"{users_text}"
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "📭 <b>Пользователи не найдены</b>\n\n"
                    "В системе еще нет зарегистрированных пользователей."
                )
        else:
            bot.send_message(
                message.chat.id,
                "❌ <b>Ошибка при получении списка пользователей!</b>"
            )
    else:
        bot.send_message(
            message.chat.id,
            f"❌ <b>Ошибка подключения к API!</b>\n\n"
            f"Причина: {response.get('error', 'Неизвестная ошибка')}"
        )

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """
    Обработчик всех остальных сообщений.
    
    Отправляет приветственное сообщение и подсказку.
    """
    user = message.from_user
    
    welcome_text = (
        f"👋 Привет, {user.first_name or 'друг'}!\n\n"
        "Я бот, интегрированный с Django REST API.\n\n"
        "Доступные команды:\n"
        "/start - Регистрация в системе\n"
        "/myinfo - Ваша информация\n"
        "/help - Справка по командам\n\n"
        "Просто выберите команду из меню или введите ее вручную."
    )
    
    bot.send_message(message.chat.id, welcome_text)
    
    logger.info(f"Сообщение от пользователя {user.id}: {message.text}")

# ==================== ЗАПУСК БОТА ====================

def check_api_connection():
    """Проверка подключения к Django API перед запуском бота."""
    logger.info("Проверка подключения к Django API...")
    
    response = send_api_request('users/', 'GET')
    
    if response['success']:
        logger.info("✅ Подключение к Django API успешно установлено")
        return True
    else:
        logger.error(f"❌ Не удалось подключиться к Django API: {response.get('error')}")
        return False

def main():
    """Основная функция для запуска бота."""
    print("=" * 50)
    print("🤖 Запуск Telegram Bot")
    print("=" * 50)
    
    # Проверка подключения к API
    if not check_api_connection():
        print("❌ Ошибка: Не удалось подключиться к Django API")
        print("Убедитесь, что сервер Django запущен:")
        print("  python manage.py runserver")
        return
    
    print(f"🌐 API URL: {API_URL}")
    print("🔗 Бот запускается...")
    print("⚠️  Для остановки бота нажмите Ctrl+C")
    print("=" * 50)
    
    try:
        # Получение информации о боте
        bot_info = bot.get_me()
        print(f"✅ Бот @{bot_info.username} успешно запущен!")
        print(f"👤 Имя бота: {bot_info.first_name}")
        print(f"🆔 ID бота: {bot_info.id}")
        print("🔄 Бот ожидает сообщений...")
        
        # Запуск бота в режиме polling
        bot.polling(none_stop=True, interval=0, timeout=20)
        
    except telebot.apihelper.ApiException as e:
        logger.error(f"Ошибка Telegram API: {e}")
        print(f"❌ Ошибка Telegram API: Проверьте токен бота")
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
        print("\n👋 Бот остановлен")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        print(f"❌ Неизвестная ошибка: {e}")

if __name__ == "__main__":
    main()