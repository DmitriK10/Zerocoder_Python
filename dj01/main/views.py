from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Это проект на Django</h1>")

def new(request):
    return HttpResponse("<h1>Это вторая страница проекта на Django</h1>")