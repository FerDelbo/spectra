from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from home.models import Aluno, FO, Turma, Colegio
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse

# --- TELA 1: DASHBOARD (Menu com os Cards das Turmas) ---
@login_required
def minhas_turmas(request):
    # Filtrar turmas do professor logado
    colegio_escolhido = Colegio.objects.filter(turma__professor=request.user).distinct()
    turmas_do_professor = Turma.objects.filter(professor=request.user)
    series_disponiveis = turmas_do_professor.values_list('serie', flat=True).distinct()
    turmas_letras = turmas_do_professor.values_list('turma', flat=True).distinct()
    alunos_filtrados = None
    turma_selecionada = None

    # Inicializar variáveis filtradas com valores padrão
    series_filtrados = series_disponiveis
    turmas_filtrados = turmas_letras

    # Verificar se há parâmetros GET para filtrar opções dinamicamente
    colegio_param = request.GET.get('colegio')
    serie_param = request.GET.get('serie')

    if colegio_param:
        # Filtrar séries com base no colégio escolhido
        series_filtrados = turmas_do_professor.filter(colegio__colegio=colegio_param).values_list('serie', flat=True).distinct()

    if serie_param and colegio_param:
        # Filtrar turmas com base na série escolhida e no colégio
        turmas_filtrados = turmas_do_professor.filter(colegio__colegio=colegio_param, serie=serie_param).values_list('turma', flat=True).distinct()

    # Processar busca quando todos os parâmetros são fornecidos
    if request.GET.get('colegio') and request.GET.get('serie') and request.GET.get('turma'):
        colegio_escolhido = request.GET.get('colegio')
        serie_escolhida = request.GET.get('serie')
        turma_escolhida = request.GET.get('turma')
        
        # Tenta achar a turma específica
        try:
            turma_obj = turmas_do_professor.get(serie=serie_escolhida, turma=turma_escolhida, colegio__colegio=colegio_escolhido)
            alunos_filtrados = Aluno.objects.filter(turma=turma_obj).order_by('nome')
            turma_selecionada = turma_obj
        except Turma.DoesNotExist:
            alunos_filtrados = []

    context = {
        'colegios_opcoes': colegio_escolhido,
        'series_opcoes': series_disponiveis,
        'turmas_opcoes': turmas_letras,
        'alunos': alunos_filtrados,
        'turma_atual': turma_selecionada,
        'series_filtrados': series_filtrados,
        'turmas_filtrados': turmas_filtrados
    }
    
    return render(request, 'minhas_turmas.html', context)

@login_required
def get_series(request):
    colegio = request.GET.get('colegio')
    if colegio:
        series = Turma.objects.filter(professor=request.user, colegio__colegio=colegio).values_list('serie', flat=True).distinct()
        return JsonResponse({'series': list(series)})
    return JsonResponse({'series': []})

@login_required
def get_turmas(request):
    colegio = request.GET.get('colegio')
    serie = request.GET.get('serie')
    if colegio and serie:
        turmas = Turma.objects.filter(professor=request.user, colegio__colegio=colegio, serie=serie).values_list('turma', flat=True).distinct()
        return JsonResponse({'turmas': list(turmas)})
    return JsonResponse({'turmas': []})

@login_required
def get_titulos(request):
    natureza = request.GET.get('natureza')
    tipo = request.GET.get('tipo')
    if natureza == 'Positivo' and tipo == 'Disciplinar':
        titulos = [choice[0] for choice in FO.TITULO_POSITIVO_DISCIPLINAR_CHOICES]
    elif natureza == 'Positivo' and tipo == 'Pedagogico':
        titulos = [choice[0] for choice in FO.TITULO_POSITIVO_PEDAGOGICO_CHOICES]
    elif natureza == 'Negativo' and tipo == 'Disciplinar':
        titulos = [choice[0] for choice in FO.TITULO_NEGATIVO_DISCIPLINAR_CHOICES]
    elif natureza == 'Negativo' and tipo == 'Pedagogico':
        titulos = [choice[0] for choice in FO.TITULO_NEGATIVO_PEDAGOGICO_CHOICES]
    else:
        titulos = []
    return JsonResponse({'titulos': titulos})

# --- AÇÃO: REGISTRAR FO ---
@login_required
def registrar_fo(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    turma = aluno.turma
    url_base = reverse('minhas_turmas')
    parametros = f"?serie={turma.serie}&turma={turma.turma}&colegio=padrao"
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
        
        return redirect(f"{url_base}{parametros}")

    return render(request, 'registrar_fo.html', {'aluno': aluno})
