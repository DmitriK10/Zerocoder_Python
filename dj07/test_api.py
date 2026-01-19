#!/usr/bin/env python3
"""
Скрипт для тестирования Django REST API.

Тестирует все эндпоинты API перед запуском бота.
Позволяет убедиться, что API работает корректно.
"""

import requests
import json
import time
import sys

API_URL = "http://127.0.0.1:8000/api"
TEST_USER_ID = 123456789  # Фиксированный ID для тестирования

def print_section(title):
    """Печать заголовка раздела"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_result(success, message, data=None):
    """Печать результата теста"""
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    
    if data:
        print(f"📊 Данные: {json.dumps(data, indent=2, ensure_ascii=False)}")

def test_connection():
    """Тест подключения к API"""
    print_section("Тест подключения к API")
    
    try:
        response = requests.get(f"{API_URL}/users/", timeout=5)
        
        if response.status_code == 200:
            print_result(True, f"Подключение успешно. Статус: {response.status_code}")
            return True
        else:
            print_result(False, f"Неверный статус: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_result(False, "Не удалось подключиться к серверу")
        return False
    except Exception as e:
        print_result(False, f"Ошибка подключения: {str(e)}")
        return False

def test_register_user():
    """Тест регистрации пользователя"""
    print_section("Тест регистрации пользователя (POST /api/register/)")
    
    test_data = {
        "user_id": TEST_USER_ID,
        "username": "test_user",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/register/",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📤 Отправлены данные: {json.dumps(test_data, indent=2)}")
        print(f"📥 Статус ответа: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print_result(True, "Пользователь успешно создан")
            print(f"🆔 User ID в базе: {data.get('data', {}).get('id')}")
            print(f"🆔 Telegram User ID: {data.get('data', {}).get('user_id')}")
            return TEST_USER_ID  # Возвращаем Telegram User ID, а не ID записи в БД
        elif response.status_code == 200:
            data = response.json()
            print_result(True, "Пользователь уже существует, данные обновлены")
            print(f"🆔 User ID в базе: {data.get('data', {}).get('id')}")
            print(f"🆔 Telegram User ID: {data.get('data', {}).get('user_id')}")
            return TEST_USER_ID  # Возвращаем Telegram User ID
        else:
            print_result(False, f"Ошибка регистрации. Статус: {response.status_code}")
            print(f"📝 Ответ сервера: {response.text}")
            return None
            
    except Exception as e:
        print_result(False, f"Ошибка при регистрации: {str(e)}")
        return None

def test_get_user(telegram_user_id):
    """Тест получения информации о пользователе"""
    print_section(f"Тест получения информации о пользователе (GET /api/user/{telegram_user_id}/)")
    print(f"🆔 Используется Telegram User ID: {telegram_user_id}")
    
    try:
        response = requests.get(f"{API_URL}/user/{telegram_user_id}/", timeout=5)
        
        print(f"📥 Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print_result(True, "Информация о пользователе получена успешно")
                print(f"👤 Имя пользователя: {data.get('data', {}).get('username')}")
                print(f"🆔 Telegram ID: {data.get('data', {}).get('user_id')}")
                return True
            else:
                print_result(False, f"Ошибка в ответе API: {data.get('message')}")
                return False
        elif response.status_code == 404:
            print_result(False, "Пользователь не найден")
            print("ℹ️  Возможные причины:")
            print("   1. Пользователь с таким Telegram ID не зарегистрирован")
            print("   2. В API передается неправильный user_id")
            print(f"   3. Ожидаемый Telegram ID: {telegram_user_id}")
            return False
        else:
            print_result(False, f"Неизвестная ошибка. Статус: {response.status_code}")
            print(f"📝 Ответ: {response.text}")
            return False
            
    except Exception as e:
        print_result(False, f"Ошибка при получении информации: {str(e)}")
        return False

def test_get_all_users():
    """Тест получения списка всех пользователей"""
    print_section("Тест получения списка пользователей (GET /api/users/)")
    
    try:
        response = requests.get(f"{API_URL}/users/", timeout=5)
        
        print(f"📥 Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print_result(True, f"Получено {count} пользователей")
            
            if count > 0:
                print("📋 Список пользователей:")
                for user in data.get('data', [])[:5]:  # Показываем только первых 5
                    print(f"  👤 @{user.get('username', 'без имени')} (ID: {user.get('user_id')})")
                if count > 5:
                    print(f"  ... и еще {count - 5} пользователей")
            
            return True
        else:
            print_result(False, f"Ошибка получения списка. Статус: {response.status_code}")
            print(f"📝 Ответ: {response.text}")
            return False
            
    except Exception as e:
        print_result(False, f"Ошибка при получении списка: {str(e)}")
        return False

def test_delete_user(telegram_user_id):
    """Тест удаления пользователя"""
    print_section(f"Тест удаления пользователя (DELETE /api/user/{telegram_user_id}/delete/)")
    print(f"⚠️  Внимание: эта операция удалит пользователя из базы данных!")
    
    confirm = input("Продолжить? (y/n): ")
    if confirm.lower() != 'y':
        print("🚫 Тест удаления отменен")
        return False
    
    try:
        response = requests.delete(f"{API_URL}/user/{telegram_user_id}/delete/", timeout=5)
        
        print(f"📥 Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            print_result(True, "Пользователь успешно удален")
            return True
        elif response.status_code == 404:
            print_result(False, "Пользователь не найден для удаления")
            return False
        else:
            print_result(False, f"Ошибка удаления. Статус: {response.status_code}")
            print(f"📝 Ответ: {response.text}")
            return False
            
    except Exception as e:
        print_result(False, f"Ошибка при удалении: {str(e)}")
        return False

def run_all_tests():
    """Запуск всех тестов"""
    print("🚀 Начало тестирования Django REST API")
    print(f"🌐 API URL: {API_URL}")
    print(f"🆔 Тестовый Telegram User ID: {TEST_USER_ID}")
    print(f"⏰ Время начала: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Результаты тестов
    results = []
    
    # Тест 1: Подключение к API
    results.append(("Подключение", test_connection()))
    
    if results[0][1]:  # Если подключение успешно
        # Тест 2: Регистрация пользователя
        telegram_user_id = test_register_user()
        if telegram_user_id:
            results.append(("Регистрация", True))
            
            # Тест 3: Получение информации о пользователе
            results.append(("Получение информации", test_get_user(telegram_user_id)))
            
            # Тест 4: Получение списка всех пользователей
            results.append(("Список пользователей", test_get_all_users()))
            
            # Тест 5: Удаление пользователя (опционально, закомментировано)
            # results.append(("Удаление", test_delete_user(telegram_user_id)))
        else:
            results.append(("Регистрация", False))
            print("❌ Регистрация не удалась, пропускаем следующие тесты")
    else:
        print("❌ Подключение не удалось, пропускаем все тесты")
    
    # Итоги тестирования
    print_section("Итоги тестирования")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"📊 Пройдено тестов: {passed}/{total}")
    
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Результат: {'ВСЕ ТЕСТЫ ПРОЙДЕНЫ' if passed == total else 'ЕСТЬ ОШИБКИ'}")
    
    if passed == total:
        print("\n🎉 Отличная работа! API работает корректно.")
        print("🤖 Теперь можно запускать Telegram бота командой: python bot_main.py")
    else:
        print("\n⚠️  Некоторые тесты не прошли. Проверьте:")
        print("   1. Запущен ли Django сервер? (python manage.py runserver)")
        print("   2. Применены ли миграции? (python manage.py migrate)")
        print("   3. Не занят ли порт 8000 другим приложением?")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Тестирование прервано пользователем")
        sys.exit(1)