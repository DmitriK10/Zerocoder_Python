import pytest
from main import init_db, add_user, get_user


@pytest.fixture
def db_conn():
    # Setup: создаем БД
    conn = init_db()
    
    # Предоставляем ресурс тесту
    yield conn
    
    # Teardown: закрываем подключение
    conn.close()


def test_add_or_get_user(db_conn):
    # Добавляем пользователя
    add_user(db_conn, "Sasha", 30)
    
    # Получаем пользователя
    user = get_user(db_conn, "Sasha")
    
    # Проверяем, что данные корректны
    # PRIMARY KEY AUTOINCREMENT создает id = 1 для первой записи
    assert user == (1, "Sasha", 30)


# Дополнительные тесты для демонстрации
def test_multiple_users(db_conn):
    """Тест работы с несколькими пользователями"""
    add_user(db_conn, "Alice", 25)
    add_user(db_conn, "Bob", 35)
    
    user1 = get_user(db_conn, "Alice")
    user2 = get_user(db_conn, "Bob")
    
    assert user1 == (1, "Alice", 25)
    assert user2 == (2, "Bob", 35)


def test_nonexistent_user(db_conn):
    """Тест поиска несуществующего пользователя"""
    user = get_user(db_conn, "Nobody")
    assert user is None  # fetchone() возвращает None если запись не найдена


# Комментарий:
# Преимущества использования фикстур:
# 1. Избегаем дублирования кода setup/teardown
# 2. Упрощаем поддержку тестов
# 3. Обеспечиваем изоляцию тестов (каждый тест получает чистую БД)
# 4. Повышаем читаемость тестов