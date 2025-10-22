import requests
import pprint

# Данные для отправки
url = "https://jsonplaceholder.typicode.com/posts"
data = {
    "title": "foo",
    "body": "bar",
    "userId": 1
}

# Отправляем POST-запрос
response = requests.post(url, json=data)  # используем json=data для корректного Content-Type

print("\nЗадание 3:")
print("Статус-код:", response.status_code)
print("Ответ сервера:")
pprint.pprint(response.json())