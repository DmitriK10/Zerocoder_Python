from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def moscow(request):
    return render(request, 'main/moscow.html')

def peter(request):
    return render(request, 'main/peter.html')

def sochi(request):
    return render(request, 'main/sochi.html')