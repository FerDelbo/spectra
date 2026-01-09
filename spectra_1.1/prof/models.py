from django.db import models
from django.contrib.auth.models import User

class UserType(models.Model):
    TIPO_CHOICES = [
        ('Professor', 'Professor'),
        ('Monitor', 'Monitor'),
        ('Pedagogo', 'Pedagogo'),
    ]
    nome = models.CharField(max_length=50, choices=TIPO_CHOICES, unique=True)
    funcoes = models.TextField(help_text="Descrição das funções deste tipo de usuário")

    def __str__(self):
        return self.nome

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Usuário")

    def __str__(self):
        return f"{self.user.username} - {self.user_type if self.user_type else 'Sem Tipo'}"