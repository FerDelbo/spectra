from django.shortcuts import render, redirect

def index(request):# Manda ele direto para o painel (home)
    if request.user.is_authenticated:
        return redirect('home') # Certifique-se que 'home' é o nome da URL do seu painel
    
    return render(request, 'maincard.html')
