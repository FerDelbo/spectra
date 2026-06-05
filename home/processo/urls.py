from django.urls import path
from . import views

urlpatterns = [
    path('', views.processo, name='processo'),
    path('detalhes/<int:fo_id>/', views.processo_detalhes, name='processo_detalhes'),
    path('media/anexo/<path:path>', views.baixar_anexo_seguro, name='baixar_anexo_seguro'),
]