from django.urls import path
from . import views
urlpatterns = [
  path('',views.prof_view, name="prof_view" ),
  ]