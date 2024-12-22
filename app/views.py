import random

import phonenumbers as ph
import requests
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from app.models import Master, MasterDaySchedule, Salon, Service, ServiceType


def index(request):
    context = {}
    return render(request, "index.html", context)


def notes(request):
    context = {}
    return render(request, "notes.html", context)


def service(request):
    masters = Master.objects.all()
    service_types = ServiceType.objects.all()
    salons = Salon.objects.all()
    context = {
        "salons": salons,
        "masters": masters,
        "service_types": service_types,
    }
    return render(request, "service.html", context)


def popup(request):
    context = {}
    return render(request, "popup.html", context)


def serviceFinally(request):
    context = {}
    return render(request, "serviceFinally.html", context)


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
