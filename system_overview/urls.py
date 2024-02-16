# system_overview/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.system_overview, name='system_overview'),
    path('general_system_overview/', views.general_system_overview, name='general_system_overview'),
    path('security_status/', views.security_status, name='security_status'),
    path('security_assessment/', views.security_assessment, name='security_assessment'),
    path('critical_alerts/', views.critical_alerts, name='critical_alerts'),
]
