from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    attractions = [
        {
            "name": "Московский Кремль",
            "city": "Москва",
            "description": "Исторический комплекс в центре Москвы, официальная резиденция Президента России.",
            "rating": 5,
            "image": "pic1.jpg"
        },
        {
            "name": "Золотые ворота",
            "city": "Владимир",
            "description": "Памятник древнерусской архитектуры, построенный в XII веке.",
            "rating": 4,
            "image": "pic2.jpg"
        },
        {
            "name": "Троице-Сергиева Лавра",
            "city": "Сергиев Посад",
            "description": "Крупнейший православный мужской монастырь России.",
            "rating": 5,
            "image": "pic3.jpg"
        }
    ]

    stats = {
        "attractions_count": 150,
        "cities_count": 45,
        "visitors": 5000000,
        "regions": 18
    }

    context = {
        "attractions": attractions,
        "stats": stats,
        "active_page": "home"  # Добавляем переменную для активной страницы
    }
    return render_template("home.html", **context)


@app.route("/about")
def about():
    team = [
        {
            "name": "Анна Иванова",
            "role": "Главный редактор",
            "description": "Специалист по культурному наследию ЦФО"
        },
        {
            "name": "Дмитрий Петров",
            "role": "Фотограф",
            "description": "Профессиональный фотограф"
        },
        {
            "name": "Мария Сидорова",
            "role": "Краевед",
            "description": "Эксперт по Центральной России"
        },
        {
            "name": "Алексей Козлов",
            "role": "Web-разработчик",
            "description": "Создатель платформы"
        }
    ]

    contacts = {
        "email": "info@хххххх.ru",
        "phone": "+7 (495) ХХХ-ХХ-ХХ",
        "address": "Москва"
    }

    context = {
        "mission": "Наша цель - сохранить и показать культурное наследие Центрального Федерального Округа для будущих поколений.",
        "team": team,
        "contacts": contacts,
        "active_page": "about"
    }
    return render_template("about.html", **context)


if __name__ == "__main__":
    app.run(debug=True)