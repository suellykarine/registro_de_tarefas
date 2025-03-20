from django.db import models


class Tarefa(models.Model):
    tarefa_id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.descricao
