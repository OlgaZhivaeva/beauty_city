import os
from datetime import date
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_city.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from app.models import Feedback, Order, Invoice, MasterDaySchedule, Master, Service, ServiceType, Salon, ClientUser, UserManager


salons = [
    {
        'title': 'BeautyCity Пушкинская',
        'address': 'ул. Пушкинская, д. 78А',
        'photo': 'salons/salon1.svg'
    },
    {
        'title': 'BeautyCity Ленина',
        'address': 'ул. Ленина, д. 211',
        'photo': 'salons/salon2.svg'
    },
    {
        'title': 'BeautyCity Красная',
        'address': 'ул. Красная, д. 10',
        'photo': 'salons/salon3.svg'
    }
]


clients = [
    {
        'full_name': 'Светлана Г.',
        'phone_number': '+7 (922) 891-14-44',
        'password': 'lol'
    },
    {
        'full_name': 'Ольга Н.',
        'phone_number': '+7 (973) 707-39-16',
        'password': 'lol'
    },
    {
        'full_name': 'Елена В.',
        'phone_number': '+7 (980) 980-43-96',
        'password': 'lol'
    },
    {
        'full_name': 'Виктория Г.',
        'phone_number': '+7 (976) 552-98-97',
        'password': 'lol'
    },
    {
        'full_name': 'Анастасия Е.',
        'phone_number': '+7 (905) 361-58-40',
        'password': 'lol'
    },
    {
        'full_name': 'Алина Ц.',
        'phone_number': '+7 (990) 436-46-74',
        'password': 'lol'
    },
]


masters = [
    {
        'full_name': 'Елизавета Лапина',
        'specialty': 'Мастер маникюра',
        'photo': 'masters/master1.svg'
    },
    {
        'full_name': 'Анастасия Сергеева',
        'specialty': 'Парикмахер',
        'photo': 'masters/master2.svg'
    },
    {
        'full_name': 'Ева Колесова',
        'specialty': 'Визажист',
        'photo': 'masters/master3.svg'
    },
    {
        'full_name': 'Мария Суворова',
        'specialty': 'Стилист',
        'photo': 'masters/master4.svg'
    },
    {
        'full_name': 'Мария Максимова',
        'specialty': 'Стилист',
        'photo': 'masters/master5.svg'
    },
    {
        'full_name': 'Майя Соболева',
        'specialty': 'Визажист',
        'photo': 'masters/master6.svg'
    }
]


feedbacks = [
    {
        'date': '2024-11-12',
        'client': 'Светлана Г.',
        'comment': 'Отличное место для красоты, очень доброжелательный и отзывчивый персонал, девочки заботливые, аккуратные и большие профессионалы. Посещаю салон с самого начала, но он не теряет своей привлекательности, как в обслуживании.'
    },
    {
        'date': '2024-11-05',
        'client': 'Ольга Н.',
        'comment': 'Мне всё лень было отзыв писать, но вот "руки дошли". Несколько раз здесь стриглась, мастера звали, кажется, Катя. Все было отлично, приятная молодая женщина и по стрижке вопросов не было)'
    },
    {
        'date': '2024-10-28',
        'client': 'Елена В.',
        'comment': 'Делала процедуру микротоки у мастера Светланы . Светлана внимательная, приветливая, ненавязчивая. Рекомендую и мастера, и процедуру. Еще делала бровки у Татьяны , я в восторге , брови просто идеально сдеданы'
    },
    {
        'date': '2024-10-13',
        'client': 'Виктория Г.',
        'comment': 'Была на педикюре у Ольги. Очень понравилось. Все инструменты стерильные, упакованы в крафт-пакет. Для меня очень важно было. Оборудование новое.'
    },
    {
        'date': '2024-10-08',
        'client': 'Анастасия Е.',
        'comment': 'Сегодня прокололи ушки дочке в этом салоне) Остались довольны обслуживанием и персоналом. Девочки очень приветливые и внимательные . Спасибо большое, всё понравилось'
    },
    {
        'date': '2024-10-01',
        'client': 'Алина Ц.',
        'comment': 'Отличный салон, сервис на самом высоком уровне, всем мастерам огромное уважение за труд, обязательно вернусь'
    }
]


service_types = [
    {
        'title': 'Услуги стилиста'
    },
    {
        'title': 'Услуги парикмахера'
    },
    {
        'title': 'Услуги мастера маникюра'
    },
    {
        'title': 'Услуги визажиста'
    }
]


servicess = [
    {
        'title': 'Маникюр',
        'type': 'Услуги мастера маникюра',
        'price': 2000,
        'duration': 90,
        'photo': 'services/service2.svg',
    },
    {
        'title': 'Педикюр',
        'type': 'Услуги мастера маникюра',
        'price': 1000,
        'duration': 60,
        'photo': 'services/service5.svg',
    },
    {
        'title': 'Стрижка волос',
        'type': 'Услуги парикмахера',
        'price': 1500,
        'duration': 60,
        'photo': 'services/service3.svg',
    },
    {
        'title': 'Окрашивание волос',
        'type': 'Услуги парикмахера',
        'price': 5000,
        'duration': 240,
        'photo': 'services/service6.svg',
    },
    {
        'title': 'Дневной макияж',
        'type': 'Услуги визажиста',
        'price': 1400,
        'duration': 30,
        'photo': 'services/service1.svg',
    },
    {
        'title': 'Вечерний макияж',
        'type': 'Услуги визажиста',
        'price': 2000,
        'duration': 60,
        'photo': 'services/service1.svg',
    },
    {
        'title': 'Укладка волос',
        'type': 'Услуги стилиста',
        'price': 3000,
        'duration': 60,
        'photo': 'services/service4.svg',
    }
]


invoices = [
    {
        'client': 'Анастасия Е.',
        'status': 'paid'
    },
    {
        'client': 'Анастасия Е.',
        'status': 'not_paid'
    },
    {
        'client': 'Алина Ц.',
        'status': 'not_paid'
    },
    {
        'client': 'Алина Ц.',
        'status': 'paid'
    },
    {
        'client': 'Ольга Н.',
        'status': 'paid'
    },
    {
        'client': 'Ольга Н.',
        'status': 'not_paid'
    }
]


orders = [
    {
        'status': 'accepted',
        'date': date.today(),
        'salon': 'BeautyCity Пушкинская',
        'client': 'Анастасия Е.',
        'master': 'Елизавета Лапина',
        'service': 'Маникюр',
        'start_at': '16:00:00',
        'invoice': 'paid'
    },
    {
        'status': 'accepted',
        'date': date.today(),
        'salon': 'BeautyCity Ленина',
        'client': 'Ольга Н.',
        'master': 'Ева Колесова',
        'service': 'Дневной макияж',
        'start_at': '18:00:00',
        'invoice': 'paid'
    },
    {
        'status': 'ended',
        'date': date.today(),
        'salon': 'BeautyCity Пушкинская',
        'client': 'Ольга Н.',
        'master': 'Ева Колесова',
        'service': 'Вечерний макияж',
        'start_at': '14:00:00',
        'invoice': 'not_paid'
    },
    {
        'status': 'ended',
        'date': date.today(),
        'salon': 'BeautyCity Красная',
        'client': 'Алина Ц.',
        'master': 'Анастасия Сергеева',
        'service': 'Окрашивание волос',
        'start_at': '12:00:00',
        'invoice': 'paid'
    },
    {
        'status': 'discard',
        'date': date.today(),
        'salon': 'BeautyCity Ленина',
        'client': 'Анастасия Е.',
        'master': 'Анастасия Сергеева',
        'service': 'Укладка волос',
        'start_at': '19:00:00',
        'invoice': 'not_paid'
    },
    {
        'status': 'accepted',
        'date': date.today(),
        'salon': 'BeautyCity Красная',
        'client': 'Алина Ц.',
        'master': 'Елизавета Лапина',
        'service': 'Маникюр',
        'start_at': '21:00:00',
        'invoice': 'not_paid'
    }
]


master_day_schedules = [
    {
        'workday': date.today(),
        'salon': 'BeautyCity Ленина',
        'master': 'Елизавета Лапина',
        'services': ['Маникюр', 'Педикюр'],
        'shift_start': '10:00:00',
        'shift_end': '19:00:00'
    },
    {
        'workday': date.today(),
        'salon': 'BeautyCity Ленина',
        'master': 'Анастасия Сергеева',
        'services': ['Окрашивание волос', 'Стрижка волос'],
        'shift_start': '10:00:00',
        'shift_end': '19:00:00'
    },
    {
        'workday': date.today(),
        'salon': 'BeautyCity Пушкинская',
        'master': 'Ева Колесова',
        'services': ['Дневной макияж', 'Вечерний макияж'],
        'shift_start': '10:00:00',
        'shift_end': '19:00:00'
    },
    {
        'workday': date.today(),
        'salon': 'BeautyCity Пушкинская',
        'master': 'Мария Суворова',
        'services': ['Укладка волос'],
        'shift_start': '10:00:00',
        'shift_end': '19:00:00'
    },
    {
        'workday': date.today(),
        'salon': 'BeautyCity Красная',
        'master': 'Мария Максимова',
        'services': ['Укладка волос'],
        'shift_start': '10:00:00',
        'shift_end': '19:00:00'
    },
    {
        'workday': date.today(),
        'salon': 'BeautyCity Красная',
        'master': 'Майя Соболева',
        'services': ['Дневной макияж', 'Вечерний макияж'],
        'shift_start': '10:00:00',
        'shift_end': '19:00:00'
    }
]


def main():
    for salon in salons:
        Salon.objects.get_or_create(
            title=salon['title'],
            address=salon['address'],
            photo=salon['photo']
        )
    for client in clients:
        ClientUser.objects.get_or_create(
            full_name=client['full_name'],
            phone_number=client['phone_number'],
            password=client['password']
        )
    for master in masters:
        Master.objects.get_or_create(
            full_name=master['full_name'],
            specialty=master['specialty'],
            photo=master['photo']
        )
    for feedback in feedbacks:
        Feedback.objects.get_or_create(
            date=feedback['date'],
            client=ClientUser.objects.get(full_name=feedback['client']),
            comment=feedback['comment']
        )
    for service_type in service_types:
        ServiceType.objects.get_or_create(
            title=service_type['title']
        )
    for service in servicess:
        Service.objects.get_or_create(
            title=service['title'],
            type=ServiceType.objects.get(title=service['type']),
            price=service['price'],
            duration=service['duration'],
            photo=service['photo']
        )
    for invoice in invoices:
        Invoice.objects.get_or_create(
            client=ClientUser.objects.get(full_name=invoice['client']),
            status=invoice['status']
        )
    for order in orders:
        client = ClientUser.objects.get(full_name=order['client'])
        Order.objects.get_or_create(
            status=order['status'],
            date=order['date'],
            salon=Salon.objects.get(title=order['salon']),
            client=client,
            master=Master.objects.get(full_name=order['master']),
            service=Service.objects.get(title=order['service']),
            start_at=order['start_at'],
            invoice=Invoice.objects.get(client=client, status=order['invoice'])
        )
    for schedule in master_day_schedules:
        master_day_schedule, created = MasterDaySchedule.objects.get_or_create(
            workday=schedule['workday'],
            salon=Salon.objects.get(title=schedule['salon']),
            master=Master.objects.get(full_name=schedule['master']),
            shift_start=schedule['shift_start'],
            shift_end=schedule['shift_end']
        )
        for service in schedule['services']:
            services = Service.objects.get(title=service)
            master_day_schedule.services.add(services)


if __name__ == "__main__":
    main()
