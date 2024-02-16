from django.urls import path
from . import views

urlpatterns = [
    path('', views.logs_monitoring, name='logs_monitoring'),

    path('system/', views.system_log, name='system logs'),
    path('kernel/', views.kernel_log, name='kernel logs'),
    path('auth/', views.auth_log, name='auth logs'),

]