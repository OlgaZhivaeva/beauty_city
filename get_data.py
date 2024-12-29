import os
import datetime
from datetime import date
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_city.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from app.models import Feedback, Order, Invoice, MasterDaySchedule, Master, Service, ServiceType, Salon, ClientUser, UserManager


order_date = '2024-12-31'
salon = 'BeautyCity Пушкинская'
client = 'Анастасия Е.'
master = 'Елизавета Лапина'
service = 'Маникюр'
start_at = '16:00:00'
status = 'not_paid'


def save_service_data_to_bd(order_date, salon, client, master, service, start_at):
    invoice = Invoice.objects.create(
        client=ClientUser.objects.get(full_name=client),
        status=status
    )
    client = ClientUser.objects.get(full_name=client)
    Order.objects.get_or_create(
        status='accepted',
        date=order_date,
        salon=Salon.objects.get(title=salon),
        client=client,
        master=Master.objects.get(full_name=master),
        service=Service.objects.get(title=service),
        start_at=start_at,
        invoice=invoice
    )


save_service_data_to_bd(order_date, salon, client, master, service, start_at)
