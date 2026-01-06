from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from home.models import Aluno, FO, Turma, Colegio
from django.contrib import messages
from django.urls import reverse

# --- TELA 1: DASHBOARD (Menu com os Cards das Turmas) ---
@login_required
def minhas_turmas(request):
    colegio_escolhido = Colegio.objects.filter(turma__professor=request.user).distinct()
    turmas_do_professor = Turma.objects.filter(professor=request.user)
    series_disponiveis = turmas_do_professor.values_list('serie', flat=True).distinct()
    turmas_letras = turmas_do_professor.values_list('turma', flat=True).distinct()
    alunos_filtrados = None
    turma_selecionada = None

    # 3. Se o usuário clicou no botão "Buscar" (GET request com parametros)
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
        'turma_atual': turma_selecionada
    }
    
    return render(request, 'minhas_turmas.html', context)

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
