import requests
from bs4 import BeautifulSoup

url = "https://example.com/table"  # адрес страницы с таблицей
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all("tr")          # все строки таблицы
data = []

for row in rows:
    cols = row.find_all("td")        # все ячейки строки
    # Удаляем пробелы и лишние символы в начале и конце текста каждой ячейки
    cleaned_cols = [col.text.strip() for col in cols]
    data.append(cleaned_cols)

print(data)