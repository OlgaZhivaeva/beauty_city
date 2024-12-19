from django.contrib import admin

from .models import (
    Client,
    Feedback,
    Invoice,
    Master,
    MasterDaySchedule,
    Order,
    Salon,
    Service,
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number")
    search_fields = ("full_name", "phone_number")
    list_filter = ("full_name",)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ("title", "address")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "duration")


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialty")


class ServiceInline(admin.TabularInline):
    model = MasterDaySchedule.services.through
    extra = 0


@admin.register(MasterDaySchedule)
class MasterDayScheduleAdmin(admin.ModelAdmin):
    list_filter = ("workday", "salon", "master")
    search_fields = ("workday", "salon", "master")
    exclude = ("services",)
    inlines = [ServiceInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("updated_at", "client", "status")
    list_filter = ("status",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("date", "status", "client", "salon", "master", "service")
    list_filter = ("date", "status", "client", "salon", "master", "service")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("date", "client")
    list_filter = ("date", "client")
