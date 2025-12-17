from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import FO, Aluno

@login_required
def meus_fos_view(request):
    meus_fos = FO.objects.filter(usuario=request.user)
    return render(request, 'meus_fos.html', {'meus_fos': meus_fos})

@login_required
def historico_aluno(request, aluno_id):
    # Pega o aluno ou dá erro 404 se não existir
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    # Pega os FOs desse aluno ordenados pela data (mais recente primeiro)
    fos = FO.objects.filter(aluno__id=aluno_id).order_by('-data_registro')
    
    
    return render(request, 'historico.html',context = {
        'aluno': aluno,
        'fos': fos
    })

def observacao_detalhes(request, fo_id):
    # Pega o registro pelo ID ou dá erro 404 se não achar
    fo = get_object_or_404(FO, id=fo_id)
    
    return render(request, 'observacao.html', {'fo': fo})