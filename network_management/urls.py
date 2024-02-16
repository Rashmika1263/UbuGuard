from django.urls import path
from . import views

urlpatterns = [
    path('', views.network_management, name='network_management'),

    path('firewall_management/', views.firewall_management, name='firewall_management'),
    # path('vpn/', views.vpn_setting, name='firewall_management'),
    # path('tor/', views.tor_setting, name='firewall_management'),
]
