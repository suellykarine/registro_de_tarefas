from django.db import models


class Tarefa(models.Model):
    TarefaID = models.AutoField(primary_key=True)
    Descricao = models.CharField(max_length=255)
    Status = models.CharField(max_length=50)
    DataCriacao = models.DateTimeField(auto_now_add=True)
    DataConclusao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.Descricao
