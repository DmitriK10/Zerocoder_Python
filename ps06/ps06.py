import csv
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
driver = webdriver.Firefox()

NAME_SELECTORS = [
    "span[itemprop='name']",
    "div[itemprop='name']",
    "meta[itemprop='name']",
    "a.ui-GPFV8",
    "*[class*='title']",
    "h3",
]

def extract_name(product_card):
    for selector in NAME_SELECTORS:
        try:
            elements = product_card.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                el = elements[0]
                if el.tag_name == 'meta':
                    name = el.get_attribute('content')
                else:
                    name = el.text
                if name and name.strip():
                    return name.strip()
        except Exception:
            continue

    try:
        img = product_card.find_element(By.CSS_SELECTOR, "img[alt]")
        alt_text = img.get_attribute('alt')
        if alt_text and alt_text.strip():
            return alt_text.strip()
    except Exception:
        pass

    return "Название не найдено"

def clean_price(price_str):
    cleaned = price_str.replace(' ', '').replace('\xa0', '')
    try:
        return int(cleaned)
    except ValueError:
        return None

try:
    url = 'https://www.divan.ru/yaroslavl/category/divany-i-kresla/'
    logging.info(f'Переход на страницу {url}')
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ProductCardMain_card__KQzzn')))
    logging.info(f'Найдено {len(products)} товаров.')

    products_data = []

    for idx, product in enumerate(products, start=1):
        try:
            name = extract_name(product)
            price_str = product.find_element(By.CSS_SELECTOR, "span.ui-LD-ZU.FullPrice_actual__Mio07").text
            price_int = clean_price(price_str)
            if price_int is None:
                logging.warning(f'Товар {idx}: не удалось преобразовать цену "{price_str}", пропускаем')
                continue

            link = product.find_element(By.CSS_SELECTOR, "a").get_attribute('href')

            logging.info(f'Товар {idx}: "{name}", цена {price_int}')
            products_data.append([name, price_int, link])

        except Exception as e:
            logging.warning(f'Ошибка при парсинге товара {idx}: {e}')
            continue

    logging.info(f'Парсинг завершен. Всего собрано товаров: {len(products_data)}')

except Exception as e:
    logging.error(f'Произошла критическая ошибка: {e}')

finally:
    driver.quit()
    logging.info('Браузер закрыт.')

csv_path = 'divan_products.csv'
try:
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена (руб)', 'Ссылка'])
        writer.writerows(products_data)
    logging.info(f'Данные успешно сохранены в файл {csv_path}')
except Exception as e:
    logging.error(f'Ошибка при сохранении файла: {e}')