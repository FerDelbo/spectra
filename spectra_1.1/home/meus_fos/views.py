from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import FO, Aluno, Anexo
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q

@login_required
def meus_fos(request):
    user_type = get_user_type(request.user)
    # 1. Filtra FOs do usuário (VERIFIQUE SE O CAMPO NO MODEL É 'usuario' OU 'autor')
    # Estou usando 'usuario' pois era o que estava na view que exibia os dados sem filtro.
    queryset = FO.objects.filter(usuario=request.user).order_by('-data_registro')

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
    # IMPORTANTE: A chave do dicionário deve ser 'meus_fos' para bater com o HTML
    context = {
        'meus_fos': queryset,
        'user_type': user_type 
    }

    # 6. Truque para manter os checkboxes marcados no HTML
    # Em vez de alterar o request.GET (que é imutável), injetamos no GET temporariamente
    # ou passamos listas extras no contexto. Vamos manter seu método de injetar no GET:
    request.GET._mutable = True
    request.GET['status_list'] = status_filter
    request.GET['natureza_list'] = natureza_filter
    request.GET._mutable = False

    return render(request, 'meus_fos.html', context)

def get_user_type(user):
    try:
        profile = user.userprofile
        return profile.user_type.nome if profile.user_type else None
    except:
        return None


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

@login_required
def observacao_detalhes(request, fo_id):
    fo = get_object_or_404(FO, id=fo_id)
    
    user_type = get_user_type(request.user)
    
    # Verificar se o usuário pode tratar este FO
    can_treat = False
    if user_type == 'Pedagogo':
        can_treat = True
    elif user_type == 'Monitor' and fo.tipo == 'Disciplinar':
        can_treat = True
    # O professor que criou pode ver, mas a lógica de tratar fica falsa por padrão acima
    
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
        # O HTML usa <input type="file" name="anexos" multiple>
        arquivos = request.FILES.getlist('anexos')
        for arquivo in arquivos:
            Anexo.objects.create(
                fo=fo,
                arquivo=arquivo,
                nome=arquivo.name # Salva o nome original do arquivo
            )

        messages.success(request, 'F.O. atualizado com sucesso!')
        return redirect('observacao_detalhes', fo_id=fo_id)
    
    # --- LÓGICA DE EXIBIÇÃO DOS ANEXOS ---
    
    # Busca todos os anexos deste FO
    todos_anexos = Anexo.objects.filter(fo=fo)
    
    # Separa em listas diferentes baseadas na extensão do arquivo
    anexos_fotos = []
    anexos_docs = []
    
    for anexo in todos_anexos:
        extensao = anexo.arquivo.name.lower().split('.')[-1]
        
        if extensao in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            anexos_fotos.append(anexo)
        elif extensao == 'pdf':
            anexos_docs.append(anexo)
        else:
            # Opcional: Se for outro tipo, decide onde colocar ou ignora
            anexos_docs.append(anexo)

    context = {
        'fo': fo,
        'can_treat': can_treat,
        'anexos_fotos': anexos_fotos, # Agora o template vai encontrar isso
        'anexos_docs': anexos_docs,   # E isso
    }
    
    return render(request, 'observacao.html', context)