from django.contrib import admin
from .models import Aluno, FO

# @admin.register já faz o registro automaticamente
# Não precisa usar admin.site.register() lá embaixo

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'turma', 'criado_em')
    search_fields = ('nome', 'turma')
    list_filter = ('turma',)
    ordering = ('nome',)

@admin.register(FO)
class FOAdmin(admin.ModelAdmin):
    list_display = ('get_aluno_nome', 'natureza', 'data_registro', 'get_aluno_turma', 'usuario')
    list_filter = ('natureza', 'data_registro', 'aluno__turma')
    search_fields = ('aluno__nome', 'usuario__username')

    @admin.display(description='Nome do Aluno', ordering='aluno__nome')
    def get_aluno_nome(self, obj):
        return obj.aluno.nome

    @admin.display(description='Turma', ordering='aluno__turma')
    def get_aluno_turma(self, obj):
        return obj.aluno.turma