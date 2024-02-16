from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'),

    path('about/', views.about, name='about'),
    path('search/', views.search_view, name='search'),

]