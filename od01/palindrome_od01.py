def is_palindrome(s):
    # шаг 1: привести строку к нижнему регистру, чтобы игнорировать регистр букв
    # шаг 2: удалить все пробелы из строки, чтобы игнорировать пробелы
    # шаг 3: получить перевернутую строку для сравнения
    # шаг 4: сравнить очищенную строку с перевернутой строкой
    # шаг 5: вернуть результат сравнения - True если строки равны, False если не равны
    
    s_lower = s.lower()
    s_clean = s_lower.replace(" ", "")
    s_reversed = s_clean[::-1]
    return s_clean == s_reversed


my_strings = ["Топот", "А роза упала на лапу Азора", "Привет мир", "Level", "мадам"]

for string in my_strings:
    result = is_palindrome(string)
    print(result)