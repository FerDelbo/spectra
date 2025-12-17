from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from home.models import Aluno, FO  # Supondo que você tenha um modelo Aluno

def index(request):
    # Como o modelo está importado, isso funciona perfeitamente:
    alunos = Aluno.objects.filter(turma="2ª A TDS")
    return render(request, 'minhas_turmas/index.html', {'alunos': alunos})

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
    # Busca o aluno pelo ID ou retorna erro 404 se não existir
    aluno = get_object_or_404(Aluno, id=aluno_id)

    if request.method == 'POST':
        natureza = request.POST.get('natureza')
        tipo = request.POST.get('tipo')
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        
        # O CAMPO MATRICULA NÃO DEVE SER ALTERADO AQUI.
        # Se você queria atualizar a matrícula do aluno, teria que ser:
        # aluno.matricula = ... e depois aluno.save(). 
        # Mas para registrar um Fato, essa linha é desnecessária. Removi.

        # 2. Cria e salva o objeto no banco de dados
        novo_fo = FO(
            usuario=request.user,  # <--- CORREÇÃO PRINCIPAL: Adicionado o usuário logado
            aluno=aluno,
            natureza=natureza,
            tipo=tipo,
            titulo=titulo,
            descricao=descricao
        )
        novo_fo.save()

        # 3. Redireciona. 
        # ATENÇÃO: Certifique-se de que a URL 'minhas_turmas' existe no urls.py.
        # Se você ainda não criou a url 'historico_aluno', mude para 'minhas_turmas' ou 'home'
        return redirect('minhas_turmas') 

    # Se for GET (apenas carregando a página)
    return render(request, 'registrar_fo.html', {'aluno': aluno})