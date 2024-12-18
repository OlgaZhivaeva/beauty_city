from django.shortcuts import render


def index(request):
    content = {}
    return render(request, 'index.html', content)


def notes(request):
    content = {}
    return render(request, 'notes.html', content)


def service(request):
    content = {}
    return render(request, 'service.html', content)


def popup(request):
    content = {}
    return render(request, 'popup.html', content)


def serviceFinally(request):
    content = {}
    return render(request, 'serviceFinally.html', content)


def manager(request):
    content = {}
    return render(request, 'admin.html', content)
