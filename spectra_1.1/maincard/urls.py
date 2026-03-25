from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 1. A rota vazia agora aponta para a Landing Page
    path('', views.index, name='maincard'),

    # 3. Rota de Login (Padrão do Django)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # ... suas outras rotas (turmas, alunos, etc) ...
]