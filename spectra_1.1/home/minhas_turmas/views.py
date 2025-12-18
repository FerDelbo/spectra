from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from home.models import Aluno, FO, Turma
from django.contrib import messages

# --- TELA 1: DASHBOARD (Menu com os Cards das Turmas) ---
@login_required
def minhas_turmas(request):
    # Busca apenas as turmas do professor logado
    turmas = Turma.objects.filter(professor=request.user).order_by('turma')
    return render(request, 'minhas_turmas.html', {'turmas': turmas})

# --- TELA 2: LISTA DE ALUNOS (Ao clicar no Card) ---
@login_required
def lista_alunos(request, turma_id):
    # 1. Busca a turma pelo ID ou dá erro 404 se não existir
    turma = get_object_or_404(Turma, id=turma_id)
    
    # 2. Busca apenas os alunos que pertencem a essa turma
    alunos = Aluno.objects.filter(turma=turma).order_by('nome')
    
    context = {
        'turma': turma,
        'alunos': alunos
    }
    
    # 3. Renderiza o template da lista de alunos
    return render(request, 'lista_alunos.html', context)

# --- AÇÃO: REGISTRAR FO ---
@login_required
def registrar_fo(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    if request.method == 'POST':
        try:
            natureza = request.POST.get('natureza')
            tipo = request.POST.get('tipo')
            titulo = request.POST.get('titulo')
            descricao = request.POST.get('descricao')

            FO.objects.create(
                usuario=request.user,
                aluno=aluno,
                natureza=natureza,
                tipo=tipo,
                titulo=titulo,
                descricao=descricao
            )
            messages.success(request, f"Fato registrado para {aluno.nome} com sucesso!")
        except Exception as e:
            # MENSAGEM DE ERRO (caso algo dê errado no código)
            messages.error(request, f'Erro ao registrar: {str(e)}')    
        
        # Volta para a lista de alunos da turma correta
        return redirect('lista_alunos', turma_id=aluno.turma.id)

    return render(request, 'registrar_fo.html', {'aluno': aluno})

@login_required
def listar_series(request):
    """
    Tela 1: Busca todas as turmas do professor e agrupa pelas Séries únicas.
    """
    series = Turma.objects.filter(professor=request.user)\
                          .values_list('serie', flat=True)\
                          .distinct()\
                          .order_by('serie')
    
    return render(request, 'listar_series.html', {'series': series})

@login_required
def listar_turmas_por_serie(request, serie_nome):
    """
    Tela 2: Mostra as turmas (A, B, C...) da série clicada anteriormente.
    """
    # Filtra turmas que pertencem ao professor E à série escolhida
    turmas = Turma.objects.filter(professor=request.user, serie=serie_nome)
    
    context = {
        'serie_atual': serie_nome,
        'turmas': turmas
    }
    # Aqui você usa o seu template antigo de minhas_turmas
    # Apenas certifique-se de que ele itera sobre 'turmas'
    return render(request, 'minhas_turmas.html', context)