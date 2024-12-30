import json
import random
from datetime import datetime

import phonenumbers as ph
import requests
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import localdate
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from app.models import Master, MasterDaySchedule, Salon, Service, ServiceType, Feedback, Order, Invoice, ClientUser
from get_data import save_service_data_to_bd

def index(request):
    masters = Master.objects.all()
    services = Service.objects.all()
    salons = Salon.objects.all()
    feedbacks = Feedback.objects.all()
    context = {
        'salons': salons,
        'services': services,
        'masters': masters,
        'feedbacks': feedbacks
    }
    return render(request, "index.html", context)


def notes(request):
    client = request.user
    new_orders = Order.objects.filter(date__gte=localdate(), client=client).order_by('-date')
    past_orders = Order.objects.filter(date__lt=localdate(), client=client).order_by('-date')
    new_orders_pay_sum = new_orders.filter(invoice__status='not_paid', status__in=['accepted', 'ended']).aggregate(pay_sum=Sum('service__price'))
    pay_summ = new_orders_pay_sum.get('pay_sum')
    print(pay_summ)
    context = {
        'pay_sum': pay_summ,
        'new_orders': new_orders,
        'past_orders': past_orders
    }

    return render(request, "notes.html", context)


@csrf_exempt
def service(request):

    masters = Master.objects.all()
    service_types = ServiceType.objects.all()
    salons = Salon.objects.all()
    context = {
        'salons': salons,
        'masters': masters,
        'service_types': service_types
    }
    return render(request, "service.html", context)



def popup(request):
    context = {}
    return render(request, "popup.html", context)


# @csrf_exempt
def service_finally(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            salon_id = data.get('salon_id')
            service_id = data.get('service_id')
            master_id = data.get('master_id')
            date = data.get('date')
            time = data.get('time')

            if not all([salon_id, service_id, master_id, date, time]):
                return JsonResponse({'message': 'Не все параметры переданы'}, status=400)

            try:
                salon = Salon.objects.get(id=salon_id)
                service = Service.objects.get(id=service_id)
                master = Master.objects.get(id=master_id)
            except Salon.DoesNotExist:
                return JsonResponse({'message': 'Некоректные данные Salon matching query does not exist.'}, status=400)
            except Service.DoesNotExist:
                return JsonResponse({'message': 'Некоректные данные Service matching query does not exist.'},
                                    status=400)
            except Master.DoesNotExist:
                return JsonResponse({'message': 'Некоректные данные Master matching query does not exist.'}, status=400)

            request.session['salon_id'] = salon_id
            request.session['service_id'] = service_id
            request.session['master_id'] = master_id
            request.session['date'] = date
            request.session['time'] = time

            return HttpResponseRedirect('/service_finally')

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Некорректный JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': 'Ошибка при обработке запроса' + str(e)}, status=400)
    elif request.method == "GET":
        salon_id = request.session.get('salon_id')
        service_id = request.session.get('service_id')
        master_id = request.session.get('master_id')
        date_str = request.session.get('date')
        time_str = request.session.get('time')

        try:
            salon = Salon.objects.get(id=salon_id)
            service = Service.objects.get(id=service_id)
            master = Master.objects.get(id=master_id)

            context = {
                'salon': salon,
                'service': service,
                'master': master,
                'selected_date': date_str,
                'selected_time': time_str,
            }
            return render(request, 'serviceFinally.html', context)
        except (Salon.DoesNotExist, Service.DoesNotExist, Master.DoesNotExist) as e:
            return JsonResponse({'message': 'Некоректные данные ' + str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'message': 'Ошибка при обработке запроса' + str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=405)


def manager(request):
    context = {}
    return render(request, "admin.html", context)


def get_masters(request):
    salon_id = request.GET.get("salon_id")
    service_id = request.GET.get("service_id")

    masters_in_salon = Master.objects.filter(
        schedules__salon_id=salon_id
    ).distinct()

    masters = masters_in_salon.filter(
        schedules__services__id=service_id
    ).distinct()

    response_data = []
    for master in masters:
        response_data.append(
            {
                "id": master.id,
                "full_name": master.full_name,
                "specialty": master.specialty,
                "photo": master.photo.url,
            }
        )

    return JsonResponse({"masters": response_data})


def generate_otp():
    return str(random.randint(1000, 9999))


def send_sms_otp(phone_number, otp):
    message = f"Код подтверждения: {otp}"
    url = "https://api.iqsms.ru/messages/v2/send/"
    payload = {
        "login": "",
        "password": "",
        "phone": phone_number,
        "text": message,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()


def normalise_phone_number(pn):
    pn_parsed = ph.parse(pn, "RU")
    if ph.is_valid_number(pn_parsed):
        pn_normalized = ph.format_number(pn_parsed, ph.PhoneNumberFormat.E164)
    else:
        raise

    return pn_normalized


class UserRegistrationView(View):
    def get(self, request):
        if not request.session.get("next_url"):
            request.session["next_url"] = request.META.get("HTTP_REFERER", "/")
        return render(request, "registration.html", {"otp_verify": False})

    def post(self, request):
        if "otp" in request.POST:
            submitted_otp = request.POST.get("otp")
            saved_otp = request.session.get("otp")

            if submitted_otp == saved_otp:
                phone_number = request.session.get("phone_number")
                full_name = request.session.get("full_name")
                User = get_user_model()
                user = User.objects.create(
                    phone_number=phone_number, full_name=full_name
                )
                user.save()
                next_url = request.session["next_url"]
                login(request, user)
                return redirect(next_url)
            else:
                messages.error(
                    request, "Неверный код подтверждения. Попробуйте еще раз"
                )
                return render(
                    request, "registration.html", {"otp_verify": False}
                )
        else:
            form_data = request.POST
            full_name = form_data["full_name"]

            try:
                phone_number = normalise_phone_number(
                    form_data["phone_number"]
                )
            except ph.phonenumberutil.NumberParseException:
                messages.error(request, "Введен неверный телефонный номер")
                return render(
                    request, "registration.html", {"otp_verify": False}
                )

            otp = generate_otp()
            # send_sms_otp(phone_number, otp)

            request.session["otp"] = otp
            request.session["phone_number"] = phone_number
            request.session["full_name"] = full_name

            return render(
                request,
                "registration.html",
                {"otp_verify": True, "otp": otp, "phone_number": phone_number},
            )


class UserLoginView(View):
    def get(self, request):
        if not request.session.get("next_url"):
            request.session["next_url"] = request.META.get("HTTP_REFERER", "/")
        return render(request, "login.html", {"otp_verify": False})

    def post(self, request):
        if "otp" in request.POST:
            submitted_otp = request.POST.get("otp")
            saved_otp = request.session.get("otp")

            if submitted_otp == saved_otp:
                phone_number = request.session["phone_number"]
                User = get_user_model()
                user = User.objects.get(phone_number=phone_number)
                next_url = request.session["next_url"]
                login(request, user)
                return redirect(next_url)
            else:
                messages.error(request, "Неверный код подтверждения. Попробуйте еще раз")
                return render(request, "login.html", {"otp_verify": False})
        else:
            try:
                phone_number = normalise_phone_number(
                    request.POST["phone_number"]
                )
            except ph.phonenumberutil.NumberParseException:
                messages.error(request, "Введен неверный телефонный номер")
                return render(request, "login.html", {"otp_verify": False})
            User = get_user_model()
            try:
                user = User.objects.get(phone_number=phone_number)
            except ObjectDoesNotExist:
                messages.error(request, "Пользователь не найден")
                return render(request, "login.html", {"otp_verify": False})
            otp = generate_otp()
            # send_sms_otp(phone_number, otp)

            request.session["otp"] = otp
            request.session["phone_number"] = phone_number

            return render(
                request,
                "login.html",
                {"otp_verify": True, "otp": otp, "phone_number": phone_number},
            )


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")


def save_to_db():
    pass


@login_required
@csrf_exempt
def create_appointment(request):
    context = {}
    if request.method == 'POST':
        salon_id = request.POST.get('salon_id')
        service_id = request.POST.get('service_id')
        master_id = request.POST.get('master_id')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        full_name = request.POST.get('fname')
        phone_number = request.POST.get('tel')
        question = request.POST.get('contactsTextarea')

        try:
            salon = Salon.objects.get(id=salon_id)
            service = Service.objects.get(id=service_id)
            master = Master.objects.get(id=master_id)

            date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()
            time_obj = datetime.strptime(time_str, '%H:%M').time()
            client = request.user

            # Сюда встасляем сохранение в базу данных
            # save_service_data_to_bd()

            invoice = Invoice.objects.create(
                client=client,
                status='not_paid'
            )
            Order.objects.get_or_create(
                status='accepted',
                date=date_obj,
                salon=salon,
                client=client,
                master=master,
                service=service,
                start_at=time_obj,
                invoice=invoice
            )

            # return render(request, 'notes.html', context)
            return HttpResponseRedirect('/notes')
        except (Salon.DoesNotExist, Service.DoesNotExist, Master.DoesNotExist) as e:
           return JsonResponse({'message': 'Некоректные данные '+str(e)}, status=400)
        except ValueError as e:
           return JsonResponse({'message': 'Неверный формат даты или времени'}, status=400)

    return JsonResponse({'message': 'Invalid request'}, status=400)
