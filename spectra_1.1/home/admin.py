from django.contrib import admin
from .models import Aluno, FO, Turma, Colegio

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'turma')
    list_filter = ('turma',)
    search_fields = ('nome', 'matricula')

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('serie', 'turma', 'ver_professores')
    search_fields = ('serie', 'turma', 'professor__first_name')# Adicione a busca para facilitar
    
    def ver_professores(self, obj):# Esta função transforma a lista de professores em um texto único (ex: "Ana, João")
        lista = obj.professor.all() # Pega todos os professores daquela turma
        return ", ".join([p.first_name for p in lista]) # Junta os nomes com vírgula
    
    ver_professores.short_description = "Professores"

@admin.register(FO)
class FOAdmin(admin.ModelAdmin):
    list_display = ('get_aluno_nome', 'natureza', 'tipo', 'data_registro', 'serie_original', 'turma_original', 'colegio_original', 'usuario', 'titulo', 'status')
    readonly_fields = [
        'data_registro', 'data_atualizacao', 'serie_original', 'turma_original', 'colegio_original',
    ]
    list_filter = ('natureza', 'tipo', 'data_registro', 'aluno__turma')
    search_fields = ('aluno__nome', 'usuario__username', 'titulo')

    @admin.display(description='Nome do Aluno', ordering='aluno__nome')
    def get_aluno_nome(self, obj):
        return obj.aluno.nome

    @admin.display(description='Turma', ordering='aluno__turma')
    def get_aluno_turma(self, obj):
        return obj.aluno.turma
    
@admin.register(Colegio)
class ColegioAdmin(admin.ModelAdmin):
    list_display = ('colegio',) # Mostra o nome na lista
    search_fields = ('colegio',) # Permite pesquisar pelo nome
