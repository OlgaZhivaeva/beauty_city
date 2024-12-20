from django.http import JsonResponse
from django.shortcuts import render

from app.models import Salon, Service, Master, ServiceType, MasterDaySchedule


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


def get_masters(request):
    salon_id = request.GET.get('salon_id')
    service_id = request.GET.get('service_id')

    # masters = MasterDaySchedule.objects.filter(salon=salon_id, services=service_id).distinct()
    masters = Master.objects.all()
    response_data = []
    for master in masters:
        response_data.append({
            'full_name': master.full_name,
            'specialty': master.specialty
        })

    return JsonResponse({'masters': response_data})

