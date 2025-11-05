#AZ03 3. Необходимо спарсить цены на диваны с сайта divan.ru в csv файл, обработать данные,
# найти среднюю цену и вывести ее, а также сделать гистограмму цен на диваны
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import matplotlib.pyplot as plt
import re

# Создаем драйвер
driver = webdriver.Chrome()

# URL страницы с диванами
url = 'https://www.divan.ru/category/divany'
print("Открываем страницу...")
driver.get(url)

# Ждем загрузки страницы
time.sleep(5)

print("Парсим цены...")

# Ищем цены по конкретным селекторам, которые работают на этом сайте
prices = []

# Основной селектор для цен
try:
    price_elements = driver.find_elements(By.CSS_SELECTOR, "span.ui-LD-ZU")
    print(f"Найдено элементов с ценами: {len(price_elements)}")

    for element in price_elements:
        price_text = element.text.strip()
        print(f"Найден текст: '{price_text}'")  # Отладка
        if price_text and ('₽' in price_text or re.search(r'\d', price_text)):
            prices.append(price_text)
except Exception as e:
    print(f"Ошибка при поиске цен: {e}")

# Если не нашли цены, пробуем альтернативный селектор
if not prices:
    try:
        print("Пробуем альтернативный селектор...")
        price_elements = driver.find_elements(By.CSS_SELECTOR, "span.price__number")
        print(f"Найдено элементов с альтернативным селектором: {len(price_elements)}")

        for element in price_elements:
            price_text = element.text.strip()
            print(f"Найден текст: '{price_text}'")  # Отладка
            if price_text and ('₽' in price_text or re.search(r'\d', price_text)):
                prices.append(price_text)
    except Exception as e:
        print(f"Ошибка при поиске альтернативных цен: {e}")

print(f"Найдено цен: {len(prices)}")
if prices:
    print("Примеры найденных цен:")
    for i, price in enumerate(prices[:5]):
        print(f"{i + 1}. {price}")
else:
    print("Цены не найдены. Используем тестовые данные.")

# Закрываем драйвер
driver.quit()

# Если цены не найдены, используем тестовые данные
if not prices:
    prices = [
        "15 000 ₽", "24 500 ₽", "32 900 ₽", "18 700 ₽", "45 000 ₽",
        "29 990 ₽", "37 500 ₽", "27 200 ₽", "55 800 ₽", "22 450 ₽",
        "38 600 ₽", "41 990 ₽", "31 800 ₽", "48 400 ₽", "36 750 ₽"
    ]
    print(" Используем тестовые данные для демонстрации")

# Сохраняем в CSV файл
with open('sofa_prices.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price'])
    for price in prices:
        writer.writerow([price])

# Очищаем цены
clean_prices = []
for price_str in prices:
    # Убираем все символы кроме цифр
    clean_price = re.sub(r'[^\d]', '', price_str)
    if clean_price:
        clean_prices.append(int(clean_price))

# Считаем среднюю цену
average_price = sum(clean_prices) / len(clean_prices)
print(f"\nСредняя цена: {average_price:.0f} рублей")

# Строим гистограмму
plt.figure(figsize=(10, 6))
plt.hist(clean_prices, bins=10, edgecolor='black')
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (рубли)')
plt.ylabel('Количество')
plt.grid(True, alpha=0.3)
plt.show()

print("\n Задание выполнено!")