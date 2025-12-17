from django.db import models
from django.contrib.auth.models import User

# --- MODELO 1: ALUNO ---
class Aluno(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    # Adicionei matricula pois seu HTML usa {{ aluno.matricula }}
    matricula = models.CharField(max_length=20, verbose_name="Matrícula", unique=True, null=True, blank=True)
    turma = models.CharField(max_length=50, verbose_name="Turma") 
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.turma}"

# --- MODELO 2: FO (Atualizado para o Formulário) ---
class FO(models.Model):
    NATUREZA_CHOICES = [
        ('Positivo', 'Positivo'),
        ('Negativo', 'Negativo'),
    ]
    
    TIPO_CHOICES = [
        ('Disciplinar', 'Disciplinar'),
        ('Pedagogico', 'Pedagógico'),
    ]

    # Relacionamentos
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Professor que registrou
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")
    
    # Campos do Formulário
    natureza = models.CharField(max_length=10, choices=NATUREZA_CHOICES)
    
    # Novo campo: Tipo (Disciplinar ou Pedagógico)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    
    # Novo campo: Título (O motivo selecionado no select, ex: "Conversa paralela")
    titulo = models.CharField(max_length=100, verbose_name="O que aconteceu?")
    
    # Descrição (Observação opcional)
    descricao = models.TextField(blank=True, null=True, verbose_name="Observação")
    # Data e Hora automáticas (não precisa vir do form)
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data do Registro")

    class Meta:
        verbose_name = "Fato Observado"
        verbose_name_plural = "Fatos Observados"
        ordering = ['-data_registro'] # Mostra os mais recentes primeiro

    def __str__(self):
        return f"{self.aluno.nome} - {self.titulo} ({self.natureza})"