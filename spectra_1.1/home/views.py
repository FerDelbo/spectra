from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FO
# Create your views here.
@login_required
def home_view(request):
    fos_recentes = FO.objects.filter(usuario=request.user).order_by('-data_registro')[:5]
    return render(request, template_name='dashboard.html', context={'fos_recentes': fos_recentes})