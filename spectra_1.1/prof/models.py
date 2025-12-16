from django.db import models

# Create your models here.
class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=128)

    REQURED_FIELDS = ['nome', 'usuario', 'senha']