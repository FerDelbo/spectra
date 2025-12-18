from django.contrib import admin
from .models import Aluno, FO, Turma

# @admin.register já faz o registro automaticamente
# Não precisa usar admin.site.register() lá embaixo

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'turma')
    list_filter = ('turma',)
    search_fields = ('nome', 'matricula')

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('serie', 'turma', 'professor')
    list_filter = ('professor',)
    search_fields = ('turma',)

@admin.register(FO)
class FOAdmin(admin.ModelAdmin):
    list_display = ('get_aluno_nome', 'natureza', 'tipo', 'data_registro', 'get_aluno_turma')
    list_filter = ('natureza', 'tipo', 'data_registro', 'aluno__turma')
    search_fields = ('aluno__nome', 'usuario__username', 'titulo')

    @admin.display(description='Nome do Aluno', ordering='aluno__nome')
    def get_aluno_nome(self, obj):
        return obj.aluno.nome

    @admin.display(description='Turma', ordering='aluno__turma')
    def get_aluno_turma(self, obj):
        return obj.aluno.turma
    
