from django.db import models
from django.contrib.auth.models import User

# --- MODELO 1: TURMA ---
# Necessário para criar os botões (A TDS, B TDS) e vincular ao Professor
class Turma(models.Model):
    serie = models.CharField(max_length=20, verbose_name="Série", blank=True, null=True)
    turma = models.CharField(max_length=50, verbose_name="Turma") # Ex: "A TDS"
    
    # Campo opcional para ajudar no título do card (ex: "2ª Série")
    
    
    professor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Professor Responsável")

    def __str__(self):
        return f"{self.turma}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"


# --- MODELO 2: ALUNO ---
class Aluno(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    
    # MANTIDO COMO 'matricula' (mas você usará para guardar a Série)
    matricula = models.CharField(max_length=20, verbose_name="Série")
    
    # Vínculo com a Turma criada acima
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.turma.turma}"


# --- MODELO 3: FO ---
class FO(models.Model):
    NATUREZA_CHOICES = [
        ('Positivo', 'Positivo'),
        ('Negativo', 'Negativo'),
    ]
    
    TIPO_CHOICES = [
        ('Disciplinar', 'Disciplinar'),
        ('Pedagogico', 'Pedagógico'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")
    
    natureza = models.CharField(max_length=10, choices=NATUREZA_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    titulo = models.CharField(max_length=100, verbose_name="O que aconteceu?")
    
    descricao = models.TextField(blank=True, null=True, verbose_name="Observação")
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data do Registro")

    class Meta:
        verbose_name = "Fato Observado"
        verbose_name_plural = "Fatos Observados"
        ordering = ['-data_registro']

    def __str__(self):
        return f"{self.aluno.nome} - {self.titulo}"