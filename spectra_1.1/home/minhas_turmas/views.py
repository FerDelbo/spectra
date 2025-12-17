from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Aluno  # Supondo que você tenha um modelo Aluno
from django.http import HttpResponse


@login_required
def minhas_turmas(request):
    # Busca os alunos do banco de dados
    alunos = Aluno.objects.all()  # Ou filtrar por turma do professor, se necessário
    
    return render(request, 'minhas_turmas.html', {
        'alunos': alunos,
        'nome_turma': '2ª A TDS'
    })

@login_required
def registrar_fo(request, aluno_id):
    # Busca o aluno no banco pelo ID
    if request.method == 'POST':
        return redirect('minhas_turmas')  # Redireciona após o envio do formulário
    aluno = get_object_or_404(Aluno, id=aluno_id)
    return render(request, 'registrar_fo.html', {
            'aluno': aluno,
            'turma_nome': '2ª A TDS'
        })

