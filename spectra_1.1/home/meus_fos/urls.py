from django.urls import path
from . import views

urlpatterns = [
    path('', views.meus_fos_view, name='meus_fos'),
]