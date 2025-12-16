from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FO

@login_required
def meus_fos_view(request):
    meus_fos = FO.objects.filter(usuario=request.user)
    return render(request, 'meus_fos.html', {'meus_fos': meus_fos})