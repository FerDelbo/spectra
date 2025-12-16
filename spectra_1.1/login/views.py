from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Tentar autenticar com username
        user = authenticate(request, username=username_or_email, password=password)
        
        if user is None:
            # Se não conseguiu com username, tentar com email
            from django.contrib.auth.models import User
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            login(request, user)
            return redirect('home')  # ou usar settings.LOGIN_REDIRECT_URL
        else:
            messages.error(request, 'Usuário/email ou senha incorretos.')
    
    return render(request, 'login.html')