from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.cache import cache  

def get_client_ip(request):
    """Função auxiliar para capturar o IP real do usuário através do Apache/Gunicorn"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        
        # --- MECÂNICA DE TRAVA DE SEGURANÇA ---
        ip = get_client_ip(request)
        cache_key = f"login_lock_{ip}_{username_or_email}"
        
        # Pega quantas tentativas erradas essa combinação já fez (padrão é 0)
        tentativas = cache.get(cache_key, 0)

        # Se já errou 3 vezes ou mais, barra antes mesmo de consultar o banco
        if tentativas >= 3:
            messages.error(request, 'Muitas tentativas de login incorretas. Seu acesso foi bloqueado por 15 minutos.')
            return render(request, 'login.html')

        # O 'authenticate' agora vai rodar o seu Custom Backend automaticamente
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            # LOGIN COM SUCESSO: Limpa o histórico de erros do cache imediatamente
            cache.delete(cache_key)
            login(request, user)
            
            next_url = request.GET.get('next')
            return redirect(next_url) if next_url else redirect('home')
        else:
            # LOGIN FALHOU: Incrementa o número de erros
            tentativas += 1
            
            # Salva o novo número de erros no cache válido por 15 minutos (900 segundos)
            cache.set(cache_key, tentativas, timeout=900)
            
            if tentativas >= 3:
                messages.error(request, 'Muitas tentativas de login incorretas. Seu acesso foi bloqueado por 15 minutos.')
            else:
                # Avisa o usuário, mas sem dizer o número de tentativas restantes para não dar pistas ao hacker
                messages.error(request, 'Usuário/email ou senha incorretos.')
    
    return render(request, 'login.html')