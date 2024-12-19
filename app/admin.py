from django.contrib import admin

from .models import Client, Salon, Service, Registration, Master, ServiceType


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # list_display = ('username', 'phone_number')
    # search_fields = ('username', 'phone_number')
    # list_filter = ('username','phone_number')
    list_display = ('username',)
    search_fields = ('username',)
    list_filter = ('username',)

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ["name", "get_services", "get_salons"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = ('title', 'type')
    list_display = ['title', 'price', 'type']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'salon', 'service', 'time_registration', 'reminder_sent', 'service_date',
                    'slot')
    list_filter = ('salon', 'master', 'client', 'service', 'reminder_sent')
    search_fields = ('salon__name', 'master__name', 'client__name', 'service__name')
    readonly_fields = ('time_registration',)

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Salon)
