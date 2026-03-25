print("Iniciando...")
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spectra.settings')
django.setup()
print("Django setup...")
from home.minhas_turmas.models import Aluno

# Adicionar alunos se não existirem
nomes = ['Claudinei Roberto Machado', 'Sebastião da Rocha', 'Edinaldo Pereira', 'Joaquim Santana', 'César Augusto', "Teresa D'Avilla", 'Henry Ford']
for nome in sorted(nomes):
    Aluno.objects.get_or_create(nome=nome, turma='2ª A TDS')

alunos = Aluno.objects.all().order_by('nome')
print(f"Encontrados {alunos.count()} alunos")
for i, aluno in enumerate(alunos, 1):
    print(f'{i}. {aluno.nome}')