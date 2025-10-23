from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time


def setup_browser():
    """Настройка браузера - выбираем Chrome или Firefox"""
    try:
        # Создаем экземпляр браузера Chrome
        browser = webdriver.Chrome()
    except:
        # Если Chrome не доступен, используем Firefox
        browser = webdriver.Firefox()
    return browser


def search_wikipedia(browser, query):
    """Поиск статьи в Википедии по запросу пользователя"""
    # Переходим на главную страницу Википедии
    browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
    time.sleep(2)

    # Находим поисковую строку по ID и вводим запрос
    search_box = browser.find_element(By.ID, "searchInput")
    search_box.clear()  # Очищаем поле ввода
    search_box.send_keys(query)  # Вводим текст запроса
    search_box.send_keys(Keys.RETURN)  # Эмулируем нажатие Enter
    time.sleep(3)

    # Если попали на страницу результатов поиска, кликаем по первой статье
    if "search" in browser.current_url:
        try:
            # Ищем первую статью в результатах поиска
            first_result = browser.find_element(By.CSS_SELECTOR, ".mw-search-result-heading a")
            first_result.click()  # Переходим по ссылке
            time.sleep(3)
        except:
            print("Не удалось найти статью по запросу")


def show_paragraphs(browser):
    """Постраничный вывод параграфов текущей статьи"""
    # Находим все параграфы на странице по тегу <p>
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    current_paragraph = 0

    # Цикл по всем параграфам с возможностью навигации
    while current_paragraph < len(paragraphs):
        # Выводим разделитель вместо очистки экрана
        print("\n" + "=" * 70)
        print(f"ПАРАГРАФ {current_paragraph + 1} ИЗ {len(paragraphs)}:")
        print("=" * 70)
        print(paragraphs[current_paragraph].text)  # Выводим текст параграфа
        print("=" * 70)

        # Проверяем, не последний ли это параграф
        if current_paragraph == len(paragraphs) - 1:
            print("\n>>> Это последний параграф статьи")
            input(">>> Нажмите Enter для возврата в меню...")
            break

        # Предлагаем пользователю выбор действия
        print("\nДоступные действия:")
        print("1 - Следующий параграф")
        print("2 - Вернуться в меню")
        choice = input("Выберите действие (1 или 2): ")

        if choice == "1":
            current_paragraph += 1  # Переход к следующему параграфу
        else:
            break  # Выход из цикла


def get_related_links(browser):
    """Получение списка связанных статей (из блоков hatnote)"""
    related_links = []
    try:
        # Ищем все ссылки в блоках с классом hatnote
        hatnotes = browser.find_elements(By.CSS_SELECTOR, ".hatnote.navigation-not-searchable a")
        for link in hatnotes:
            href = link.get_attribute("href")  # Получаем URL ссылки
            # Обрезаем длинный текст для удобства отображения
            text = link.text[:80] + "..." if len(link.text) > 80 else link.text
            if href and "wikipedia.org" in href:
                related_links.append((text, href))  # Добавляем в список
    except:
        # Игнорируем ошибки если блоков нет
        pass
    return related_links


def show_related_articles(browser):
    """Показать связанные статьи и перейти по выбору пользователя"""
    links = get_related_links(browser)

    if not links:
        print("\n>>> Связанные статьи не найдены")
        time.sleep(2)
        return None

    while True:
        # Выводим разделитель вместо очистки экрана
        print("\n" + "=" * 70)
        print("СВЯЗАННЫЕ СТАТЬИ:")
        print("=" * 70)

        # Выводим пронумерованный список связанных статей
        for i, (text, href) in enumerate(links, 1):
            print(f"{i}. {text}")
        print(f"{len(links) + 1}. Вернуться в меню")
        print("=" * 70)

        try:
            choice = int(input("\nВыберите статью (введите номер): "))
            # Обрабатываем выбор пользователя
            if 1 <= choice <= len(links):
                print(f">>> Переход к статье: {links[choice - 1][0]}")
                browser.get(links[choice - 1][1])  # Переходим по выбранной ссылке
                time.sleep(3)
                return True
            elif choice == len(links) + 1:
                return False  # Возврат в меню
            else:
                print(">>> Неверный выбор. Пожалуйста, выберите номер из списка.")
                time.sleep(1)
        except ValueError:
            print(">>> Ошибка: введите число, соответствующее номеру статьи.")
            time.sleep(1)


def display_current_article_info(browser):
    """Отображает информацию о текущей статье"""
    print("\n" + "=" * 70)
    print("ТЕКУЩАЯ СТАТЬЯ:")
    print("=" * 70)
    print(f"Название: {browser.title}")
    print("=" * 70)


def main_menu():
    """Отображает главное меню"""
    print("\n" + "=" * 70)
    print("ГЛАВНОЕ МЕНЮ:")
    print("=" * 70)
    print("1. Листать параграфы текущей статьи")
    print("2. Перейти на связанную статью")
    print("3. Выйти из программы")
    print("=" * 70)


def main():
    """Основная функция программы"""
    # Инициализируем браузер
    browser = setup_browser()

    try:
        # Получаем первоначальный запрос от пользователя
        print("=" * 70)
        print("ПОИСК В ВИКИПЕДИИ")
        print("=" * 70)
        query = input("Введите запрос для поиска в Википедии: ")

        # Выполняем поиск по запросу
        search_wikipedia(browser, query)

        # Основной цикл программы
        while True:
            # Отображаем информацию о текущей статье
            display_current_article_info(browser)

            # Показываем главное меню
            main_menu()

            # Получаем выбор пользователя
            choice = input("Выберите действие (1-3): ")

            # Обрабатываем выбор пользователя
            if choice == "1":
                show_paragraphs(browser)  # Показ параграфов текущей статьи
            elif choice == "2":
                # Переход к связанным статьям
                if not show_related_articles(browser):
                    continue  # Продолжаем цикл если пользователь вернулся в меню
            elif choice == "3":
                # Выход из программы
                print("\n>>> Завершение работы программы...")
                break
            else:
                print(">>> Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
                time.sleep(1)

    except Exception as e:
        # Обработка неожиданных ошибок
        print(f">>> Произошла ошибка: {e}")
    finally:
        # Всегда закрываем браузер даже при ошибках
        print(">>> Закрытие браузера...")
        browser.quit()


# Запуск программы
if __name__ == "__main__":
    main()