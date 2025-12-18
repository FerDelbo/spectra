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
    # Pega a turma pelo ID
    turma_selecionada = get_object_or_404(Turma, id=turma_id)

    # SEGURANÇA: Se a turma não for desse professor, volta pro menu
    if turma_selecionada.professor != request.user:
        return redirect('minhas_turmas')

    # Pega os alunos dessa turma específica
    alunos = Aluno.objects.filter(turma=turma_selecionada)

    return render(request, 'lista_alunos.html', {
        'turma': turma_selecionada,
        'alunos': alunos
    })

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