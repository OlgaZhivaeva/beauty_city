from django.shortcuts import render

from app.models import Salon, Service, Master, ServiceType


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
    if request.is_ajax() and request.method == 'POST':
        salon_id = request.POST.get('salon_id')
        service_id = request.POST.get('service_id')

        # Проверяем, что переданы оба параметра
        if salon_id is not None and service_id is not None:
            try:
                salon = Salon.objects.get(id=int(salon_id))
                service = Service.objects.get(id=int(service_id))
            except (Salon.DoesNotExist, ValueError):
                return JsonResponse({'error': 'Неверный идентификатор салона'}, status=400)
            except (Service.DoesNotExist, ValueError):
                return JsonResponse({'error': 'Неверный идентификатор услуги'}, status=400)

            # Получение мастеров, работающих в данном салоне и предоставляющих данную услугу
            masters = Master.objects.filter(salons=salon, services=service).values('id', 'full_name', 'specialty')

            return JsonResponse(list(masters), safe=False)
        else:
            return JsonResponse({'error': 'Не все параметры были переданы'}, status=400)
    else:
        return JsonResponse({'error': 'Неправильный метод запроса'}, status=400)