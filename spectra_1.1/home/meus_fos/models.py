from django.db import models
from django.contrib.auth.models import User

class FO(models.Model):
    NATUREZA_CHOICES = [
        ('Positivo', 'Positivo'),
        ('Negativo', 'Negativo'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    natureza = models.CharField(max_length=10, choices=NATUREZA_CHOICES)
    nome_aluno = models.CharField(max_length=100)
    turno = models.CharField(max_length=20)
    serie = models.CharField(max_length=20)
    turma = models.CharField(max_length=20)
    data = models.DateField()

    def __str__(self):
        return f"{self.nome_aluno} - {self.natureza}"
