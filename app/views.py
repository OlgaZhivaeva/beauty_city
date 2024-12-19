from django.shortcuts import render

from app.models import Salon, Service, Master


def index(request):
    context = {}
    return render(request, 'index.html', context)


def notes(request):
    context = {}
    return render(request, 'notes.html', context)


def service(request):
    masters = Master.objects.all()
    service_types = ServiceType.objects.all()
    salons = Salon.objects.all()
    context = {
        'salons': salons,
        'masters': masters,
        'service_types': service_types
    }
    return render(request, 'service.html', context)


def popup(request):
    context = {}
    return render(request, 'popup.html', context)


def serviceFinally(request):
    context = {}
    return render(request, 'serviceFinally.html', context)


def manager(request):
    context = {}
    return render(request, 'admin.html', context)
