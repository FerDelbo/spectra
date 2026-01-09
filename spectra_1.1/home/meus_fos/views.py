from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import FO, Aluno
from django.contrib import messages
from django.shortcuts import redirect
from prof.models import UserProfile

def get_user_type(user):
    try:
        profile = user.userprofile
        return profile.user_type.nome if profile.user_type else None
    except:
        return None

@login_required
def meus_fos_view(request):
    # Mostra apenas os F.O.'s que o usuário registrou
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
    
    user_type = get_user_type(request.user)
    
    # Verificar se o usuário pode tratar este FO
    can_treat = False
    if user_type == 'Pedagogo':
        can_treat = True
    elif user_type == 'Monitor' and fo.tipo == 'Disciplinar':
        can_treat = True
    elif user_type == 'Professor' and fo.usuario == request.user:
        # Professores só veem os próprios, mas não tratam
        can_treat = False
    
    if request.method == 'POST' and can_treat:
        status = request.POST.get('status')
        relatorio = request.POST.get('relatorio')
        evidencias = request.POST.get('evidencias')
        
        fo.status = status
        fo.relatorio = relatorio
        fo.evidencias = evidencias
        if status == 'Em andamento' and not fo.responsavel:
            fo.responsavel = request.user
        fo.save()
        messages.success(request, 'F.O. atualizado com sucesso!')
        return redirect('observacao_detalhes', fo_id=fo_id)
    
    return render(request, 'observacao.html', {'fo': fo, 'can_treat': can_treat})