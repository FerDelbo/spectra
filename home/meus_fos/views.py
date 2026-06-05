import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from home.models import FO, Aluno, Anexo
from django.contrib import messages
from django.db.models import Q

def get_user_type(user):
    try:
        profile = user.userprofile
        return profile.user_type.nome if profile.user_type else None
    except:
        return None

def get_user_colegios(user):
    try:
        profile = user.userprofile
        return profile.colegios.all()
    except AttributeError:
        return []

@login_required
def meus_fos(request):
    user_type = get_user_type(request.user)
    colegios_usuario = get_user_colegios(request.user)
    
    # 1. Filtra apenas os FOs criados pelo próprio usuário LOGADO
    # Adicionamos também a trava de colégio por segurança redundante
    queryset = FO.objects.filter(
        usuario=request.user,
        aluno__turma__colegio__in=colegios_usuario
    ).order_by('-data_registro')

    # 2. Pesquisa (Nome, Turma, Tipo)
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(aluno__nome__icontains=search_query) |
            Q(aluno__turma__turma__icontains=search_query) |
            Q(tipo__icontains=search_query)
        )

    # 3. Filtros de Checkbox (Status)
    status_filter = request.GET.getlist('status')
    if status_filter:
        queryset = queryset.filter(status__in=status_filter)

    # 4. Filtros de Checkbox (Natureza)
    natureza_filter = request.GET.getlist('natureza')
    if natureza_filter:
        queryset = queryset.filter(natureza__in=natureza_filter)

    # 5. Prepara o contexto
    context = {
        'meus_fos': queryset,
        'user_type': user_type 
    }

    # 6. Truque para manter os checkboxes marcados no HTML
    request.GET._mutable = True
    request.GET['status_list'] = status_filter
    request.GET['natureza_list'] = natureza_filter
    request.GET._mutable = False

    return render(request, 'meus_fos.html', context)


@login_required
def historico_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    colegios_usuario = get_user_colegios(request.user)
    user_type = get_user_type(request.user)
    
    # === MECÂNICA DE SEGURANÇA ADICIONADA ===
    # 1. Verifica se o Aluno pertence a algum colégio vinculado ao usuário
    if aluno.turma.colegio not in colegios_usuario:
        messages.error(request, 'Acesso negado: Este aluno pertence a outra instituição.')
        return redirect('meus_fos')
        
    # 2. Filtra os FOs desse aluno respeitando o tipo de usuário
    fos = FO.objects.filter(aluno=aluno).order_by('-data_registro')
    
    if user_type == 'Monitor':
        fos = fos.filter(tipo='Disciplinar')
    elif user_type == 'Professor':
        # Professor só vê o histórico do aluno referente aos FOs que ele mesmo abriu
        fos = fos.filter(usuario=request.user)
    
    return render(request, 'historico.html', {
        'aluno': aluno,
        'fos': fos
    })


@login_required
def observacao_detalhes(request, fo_id):
    fo = get_object_or_404(FO, id=fo_id)
    user_type = get_user_type(request.user)
    colegios_usuario = get_user_colegios(request.user)
    
    # === MECÂNICA DE SEGURANÇA ADICIONADA ===
    # 1. Trava de Colégio
    if fo.aluno.turma.colegio not in colegios_usuario:
        messages.error(request, 'Acesso negado: Este processo pertence a outra instituição.')
        return redirect('meus_fos')
        
    # 2. Trava de Permissão de Visualização básica
    can_view = False
    if user_type == 'Pedagogo':
        can_view = True
    elif user_type == 'Monitor' and fo.tipo == 'Disciplinar':
        can_view = True
    elif user_type == 'Professor' and fo.usuario == request.user:
        can_view = True
        
    if not can_view:
        messages.error(request, 'Acesso negado para o seu tipo de usuário.')
        return redirect('meus_fos')
    
    # 3. Lógica de permissão de alteração (Tratamento)
    can_treat = False
    if fo.status not in ['Concluído', 'Anulado']:
        if user_type == 'Pedagogo' or (user_type == 'Monitor' and fo.tipo == 'Disciplinar'):
            can_treat = True
    
    # Processamento do POST (Salvar alterações / Upload / Excluir)
    if request.method == 'POST' and can_treat:
        # 1. Lógica de Exclusão de Anexo
        if 'excluir_anexo' in request.POST:
            anexo_id = request.POST.get('anexo_id')
            anexo = get_object_or_404(Anexo, id=anexo_id, fo=fo)
            anexo.delete()
            messages.success(request, 'Anexo removido com sucesso.')
            return redirect('observacao_detalhes', fo_id=fo_id)

        # 2. Atualização dos dados do FO
        status = request.POST.get('status')
        relatorio = request.POST.get('relatorio')
        
        fo.status = status
        fo.relatorio = relatorio
        
        # Se mudou para "Em andamento" e não tinha dono, assume o usuário atual
        if status == 'Em andamento' and not fo.responsavel:
            fo.responsavel = request.user
            
        fo.save()

        # 3. Upload de Novos Arquivos
        arquivos = request.FILES.getlist('anexos')
        for arquivo in arquivos:
            # Validação simples de tamanho (Opcional, mas recomendado: Limite 5MB)
            if arquivo.size <= 5 * 1024 * 1024:
                Anexo.objects.create(
                    fo=fo,
                    arquivo=arquivo,
                    nome=arquivo.name
                )

        messages.success(request, 'F.O. atualizado com sucesso!')
        return redirect('observacao_detalhes', fo_id=fo_id)
    
    # --- LÓGICA DE EXIBIÇÃO DOS ANEXOS ---
    todos_anexos = Anexo.objects.filter(fo=fo)
    anexos_fotos = []
    anexos_docs = []
    
    for anexo in todos_anexos:
        extensao = anexo.arquivo.name.lower().split('.')[-1]
        if extensao in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            anexos_fotos.append(anexo)
        else:
            anexos_docs.append(anexo)

    context = {
        'fo': fo,
        'can_treat': can_treat,
        'anexos_fotos': anexos_fotos,
        'anexos_docs': anexos_docs,
        'user_type': user_type
    }
    
    return render(request, 'observacao.html', context)