from django.urls import path, include
from . import views
from home import views as home_views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('processo/', include('home.processo.urls')),
]