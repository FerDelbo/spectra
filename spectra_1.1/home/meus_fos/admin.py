from django.contrib import admin
from .models import FO

@admin.register(FO)
class FOAdmin(admin.ModelAdmin):
    list_display = ('nome_aluno', 'natureza', 'turno', 'serie', 'turma', 'data')
    list_filter = ('natureza', 'turno', 'serie', 'turma', 'data')
