from django.http import HttpResponse

def data(request):
    return HttpResponse("<h1>Страница data приложения dj01</h1><p>Это страница с данными.</p>")

def test(request):
    return HttpResponse("<h1>Страница test приложения dj01</h1><p>Это тестовая страница.</p>")