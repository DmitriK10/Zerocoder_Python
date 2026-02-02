import sqlite3


def init_db():
    conn = sqlite3.connect(':memory:')  # Создаем БД в памяти
    cursor = conn.cursor()
    
    # Создаем таблицу users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER
        )
    ''')
    
    return conn  # Возвращаем подключение


def add_user(conn, name, age):
    cursor = conn.cursor()
    # Используем параметризованный запрос для безопасности
    cursor.execute('''
        INSERT INTO users (name, age) VALUES (?, ?)
    ''', (name, age))
    conn.commit()  # Сохраняем изменения


def get_user(conn, name):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE name=?
    ''', (name,))
    return cursor.fetchone()  # Возвращаем первую найденную запись