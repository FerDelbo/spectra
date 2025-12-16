from django.db import models


class Aluno(models.Model):
    # O nome do aluno
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    
    # A turma a que ele pertence (importante para filtrar depois)
    # Ex: "2ª A TDS"
    turma = models.CharField(max_length=50, verbose_name="Turma")

    # Data de cadastro (opcional, mas boa prática)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.turma}"

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        # ESTA LINHA É O SEGREDO:
        # Ela garante que o banco sempre entregue a lista em ordem alfabética
        ordering = ['nome']