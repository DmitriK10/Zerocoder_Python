import requests
import pprint

# Отправляем GET-запрос к GitHub API для поиска репозиториев с кодом на HTML
url = "https://api.github.com/search/repositories"
params = {"q": "language:html"}

response = requests.get(url, params=params)

# Выводим статус-код
print("Задание 1:")
print("Статус-код:", response.status_code)

# Выводим ответ в формате JSON 
pprint.pprint(response.json())