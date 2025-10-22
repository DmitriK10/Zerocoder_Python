import requests
import pprint

# Отправляем GET-запрос к JSONPlaceholder с фильтром по userId=1
url = "https://jsonplaceholder.typicode.com/posts"
params = {"userId": 1}

response = requests.get(url, params=params)

print("\nЗадание 2:")
print("Статус-код:", response.status_code)
print("Посты пользователя с userId=1:")
pprint.pprint(response.json())