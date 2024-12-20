"""
URL configuration for beauty_city project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('manager/', views.manager, name='manager'),
    path('notes/', views.notes, name='notes'),
    path('service/', views.service, name='service'),
    path('popup/', views.popup, name='popup'),
    path('serviceFinally/', views.serviceFinally, name='serviceFinally'),
    path('get_masters/', views.get_masters, name='get_masters'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
