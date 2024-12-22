from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app.models import Salon, Service, Master, ServiceType, MasterDaySchedule


def index(request):
    context = {}
    return render(request, 'index.html', context)


def notes(request):
    context = {}
    return render(request, 'notes.html', context)


@csrf_exempt
def service(request):
    if request.method == 'POST':
        salon_id = request.POST.get('salon_id')
        service_id = request.POST.get('service_id')
        master_id = request.POST.get('master_id')

        if not all([salon_id, service_id, master_id]):
            return JsonResponse({'status': 'error', 'message': 'Не все поля заполнены'})

        try:
            Salon.objects.get(id=salon_id)
            Service.objects.get(id=service_id)
            Master.objects.get(id=master_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Некорректные идентификаторы'})

        context = {
            'salon_id': salon_id,
            'service_id': service_id,
            'master_id': master_id,
        }
        return render(request, 'serviceFinally.html', context)

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


@csrf_exempt
def serviceFinally(request):
    context = {}
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        salon_id = request.POST.get('salon_id')
        service_id = request.POST.get('service_id')
        master_id = request.POST.get('master_id')
        selected_date = request.POST.get('selected_date')
        # selected_time = request.POST.get('selected_time')

        if not all([salon_id, service_id, master_id, selected_date]):
            context['error'] = 'Не все данные переданы'
            return render(request, 'index.html', context)

        try:
            salon_id = int(salon_id)
            service_id = int(service_id)
            master_id = int(master_id)

            salon = Salon.objects.filter(id=salon_id)
            service = Service.objects.filter(id=service_id)
            master = Master.objects.filter(id=master_id)

            context = {
                'salon': salon,
                'service': service,
                'master': master,
                # 'selected_date': selected_date,
                # 'selected_time': selected_time
            }

            return render(request, 'serviceFinally.html', context)
        except Exception as e:
            context = {}
            return render(request, 'serviceFinally.html', context)
    else:
        return HttpResponseRedirect('service')



def manager(request):
    context = {}
    return render(request, 'admin.html', context)


def get_masters(request):
    salon_id = request.GET.get('salon_id')
    service_id = request.GET.get('service_id')

    masters_in_salon = Master.objects.filter(schedules__salon_id=salon_id).distinct()

    masters = masters_in_salon.filter(schedules__services__id=service_id).distinct()

    response_data = []
    for master in masters:
        response_data.append({
            'full_name': master.full_name,
            'specialty': master.specialty,
            'photo': master.photo.url,
        })

    return JsonResponse({'masters': response_data})