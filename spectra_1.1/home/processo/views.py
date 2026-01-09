from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import FO, FOHistory
from prof.models import UserProfile
from django.contrib import messages
from django.shortcuts import redirect

def get_user_type(user):
    try:
        profile = user.userprofile
        return profile.user_type.nome if profile.user_type else None
    except:
        return None

@login_required
def processo_view(request):
    user_type = get_user_type(request.user)
    
    # Filtrar F.O. baseados no tipo de usuário
    if user_type == 'Professor':
        # Professores veem apenas os próprios F.O.
        fos = FO.objects.filter(usuario=request.user)
    elif user_type == 'Monitor':
        # Monitores veem F.O. de tipo Disciplinar
        fos = FO.objects.filter(tipo='Disciplinar')
    elif user_type == 'Pedagogo':
        # Pedagogos veem todos os F.O.
        fos = FO.objects.all()
    else:
        fos = FO.objects.none()
    
    return render(request, 'processo.html', {'fos': fos})

@login_required
def processo_detalhes(request, fo_id):
    fo = get_object_or_404(FO, id=fo_id)
    user_type = get_user_type(request.user)
    
    # 1. Verificação de Acesso
    can_view = False
    if user_type == 'Professor' and fo.usuario == request.user:
        can_view = True
    elif user_type == 'Monitor' and fo.tipo == 'Disciplinar':
        can_view = True
    elif user_type == 'Pedagogo':
        can_view = True
    
    if not can_view:
        messages.error(request, 'Acesso negado.')
        return redirect('processo')

    # 2. Lógica de Reabertura
    if request.method == 'POST' and 'reabrir_caso' in request.POST:
        if user_type == 'Pedagogo' or (user_type == 'Monitor' and fo.tipo == 'Disciplinar'):
            FOHistory.objects.create(
                fo=fo,
                usuario=request.user,
                campo_alterado='status',
                valor_anterior=fo.status,
                valor_novo='Em andamento',
                descricao='Caso reaberto para revisão.'
            )
            fo.status = 'Em andamento'
            fo.save()
            messages.success(request, 'Processo reaberto!')
            return redirect('processo_detalhes', fo_id=fo.id)

    # 3. Lógica de permissão de edição (Tratativa)
    # Se estiver concluído, ninguém edita (can_treat = False)
    can_treat = False
    if fo.status != 'Concluído':
        if user_type == 'Pedagogo' or (user_type == 'Monitor' and fo.tipo == 'Disciplinar'):
            can_treat = True

    # 4. Salvar Alterações e Gerar Histórico (Apenas o que mudou)
    if request.method == 'POST' and can_treat and 'reabrir_caso' not in request.POST:
        new_status = request.POST.get('status')
        new_relatorio = request.POST.get('relatorio', '').strip()
        new_evidencias = request.POST.get('evidencias', '').strip()
        
        has_changes = False

        # Verifica mudança no Status
        if fo.status != new_status:
            FOHistory.objects.create(
                fo=fo, usuario=request.user, campo_alterado='status',
                valor_anterior=fo.status, valor_novo=new_status,
                descricao=f'Status alterado para {new_status}.'
            )
            fo.status = new_status
            has_changes = True

        # Verifica mudança no Relatório (Compara strings limpas)
        old_relatorio = (fo.relatorio or '').strip()
        if old_relatorio != new_relatorio:
            FOHistory.objects.create(
                fo=fo, usuario=request.user, campo_alterado='relatorio',
                valor_anterior=old_relatorio, valor_novo=new_relatorio,
                descricao='O relatório técnico foi atualizado.'
            )
            fo.relatorio = new_relatorio
            has_changes = True

        # Verifica mudança nas Evidências
        old_evidencias = (fo.evidencias or '').strip()
        if old_evidencias != new_evidencias:
            FOHistory.objects.create(
                fo=fo, usuario=request.user, campo_alterado='evidencias',
                valor_anterior=old_evidencias, valor_novo=new_evidencias,
                descricao='Novas evidências ou links foram anexados.'
            )
            fo.evidencias = new_evidencias
            has_changes = True

        if has_changes:
            fo.responsavel = request.user
            fo.save()
            messages.success(request, 'F.O. atualizada com sucesso!')
        else:
            messages.info(request, 'Nenhuma alteração detectada.')
            
        return redirect('processo')

    return render(request, 'processo_detalhes.html', {
        'fo': fo, 
        'can_treat': can_treat, 
        'user_type': user_type
    })
