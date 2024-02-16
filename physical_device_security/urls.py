from django.urls import path
from . import views

urlpatterns = [
    path('', views.physical_security, name='physical_device_security'),

    path('usb/', views.usb, name='usb'),

]
