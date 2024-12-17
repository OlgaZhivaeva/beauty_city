from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

# def notes():


def service(request):
    content = {}
    return render(request, 'service.html', content)

# def popup():
    
    
# def serviceFinally():


def manager(request):
    content = {}
    return render(request, 'admin.html', content)
