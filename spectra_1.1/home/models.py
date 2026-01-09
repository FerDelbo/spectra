from django.db import models
from django.contrib.auth.models import User

# --- MODELO 1: TURMA ---
# Necessário para criar os botões (A TDS, B TDS) e vincular ao Professor
class Turma(models.Model):
    serie_choices = [
        ('6º', '6º'),
        ('7º', '7º'),
        ('8º', '8º'),
        ('9º', '9º'),
        ('1ª', '1ª'),
        ('2ª', '2ª'),
        ('3ª', '3ª'),
    ]
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE, verbose_name="Colégio", blank=True, null=True)
    serie = models.CharField(max_length=20, verbose_name="Série", choices=serie_choices)
    turma = models.CharField(max_length=50, verbose_name="Turma") # Ex: "A TDS"
    professor = models.ManyToManyField(User, verbose_name="Professores Responsáveis", related_name="turmas")

    def __str__(self):
        return f"{self.get_serie_display()} - {self.turma}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        unique_together = ('serie', 'turma', 'colegio')


# --- MODELO 2: ALUNO ---
class Aluno(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    # MANTIDO COMO 'matricula' (mas você usará para guardar a Série)
    matricula = models.CharField(max_length=20, verbose_name="Série")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE, verbose_name="Colégio")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.turma}"


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

    TITULO_CHOICES = [
        ('Participação em aula', 'Participação em aula'),
        ('Comportamento exemplar', 'Comportamento exemplar'),
        ('Atraso', 'Atraso'),
        ('Falta de material', 'Falta de material'),
        ('Distração', 'Distração'),
        ('Outro', 'Outro'),
    ]

    TITULO_POSITIVO_DISCIPLINAR_CHOICES = [
        ('Cumpriu ativamente com todas as atribuições, quando Chefe de Turma e ou Subchefe de Turma', 'Cumpriu ativamente com todas as atribuições, quando Chefe de Turma e ou Subchefe de Turma'),
        ('Outro', 'Outro'),
    ]

    TITULO_POSITIVO_PEDAGOGICO_CHOICES = [
        ('Participação em aula', 'Participação em aula'),
        ('Outro', 'Outro'),
    ]

    TITULO_NEGATIVO_DISCIPLINAR_CHOICES = [
        ('Distração', 'Distração'),
        ('Outro', 'Outro'),
    ]

    TITULO_NEGATIVO_PEDAGOGICO_CHOICES = [
        ('Atraso', 'Atraso'),
        ('Falta de material', 'Falta de material'),
        ('Outro', 'Outro'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE, verbose_name="Colégio", blank=True, null=True)
    natureza = models.CharField(max_length=10, choices=NATUREZA_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    titulo = models.CharField(max_length=100, verbose_name="O que aconteceu?", choices=TITULO_CHOICES)
    descricao = models.TextField(blank=True, null=True, verbose_name="Observação")
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data do Registro")

    class Meta:
        verbose_name = "Fato Observado"
        verbose_name_plural = "Fatos Observados"
        ordering = ['-data_registro']

    def __str__(self):
        return f"{self.aluno.nome} - {self.titulo}"
    
class Colegio(models.Model):
    colegio = models.CharField(max_length=100, verbose_name="Nome do Colégio", blank=True, default="")
    def __str__(self):
        return self.colegio

    class Meta:
        verbose_name = "Colégio"
        verbose_name_plural = "Colégios"
