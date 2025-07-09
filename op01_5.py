#5. Написать конвертер валюты. Эта программа будет конвертировать введённую пользователем сумму в другую валюту. Курс валюты можно ввести самостоятельно и один раз.
exchange_rate = 90.5  # Курс доллара к рублю
usd_amount = float(input("Введите сумму в USD: "))

rub_amount = usd_amount * exchange_rate
print(f"{usd_amount} USD = {rub_amount:.2f} RUB")
print();