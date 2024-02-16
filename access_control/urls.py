# access_control/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.access_control, name='user_access_management'),

    path('user_access_management/', views.user_access_management, name='user_access_management'),
    
    path('user_access_management/uam', views.uam, name='user_access_management'),
    path('user_access_management/pam',views.pam, name='previlege_access_management'),
    path('user_access_management/ua', views.ua, name='user_activity'),
    path('user_access_management/ul', views.ul, name='user_last_login'),

    path('ssh_management/', views.ssh_management, name='ssh_management'),
    path('ssh_management/conf', views.ssh_conf, name='ssh_configurations'),

    path('ubugaurd_authentication/', views.ubugaurd_authentication, name='ubugaurd_authentication'),
    path('ubugaurd_authentication/passwd', views.ubugaurd_passwd, name='ubugaurd_passwd'),
    path('ubugaurd_authentication/email', views.ubugaurd_email, name='ubugaurd_email'),

]
