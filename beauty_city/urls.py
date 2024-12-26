from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("manager/", views.manager, name="manager"),
    path("notes/", views.notes, name="notes"),
    path("service/", views.service, name="service"),
    path("popup/", views.popup, name="popup"),
    path("serviceFinally/", views.service_finally, name="serviceFinally"),
    path("get_masters/", views.get_masters, name="get_masters"),
    path(
        "register/",
        views.UserRegistrationView.as_view(),
        name="user_registration",
    ),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
    path('pre_appointment/', views.pre_appointment, name='pre_appointment'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
