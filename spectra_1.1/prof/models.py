from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=128)

    REQURED_FIELDS = ['nome', 'usuario', 'senha']

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Usuário")

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()