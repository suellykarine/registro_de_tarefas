from django.urls import path

from . import views
from .views import (
    atualizar_status,
    criar_tarefa,
    excluir_tarefa,
    listar_tarefas,
    relatorio_tarefas,
)

urlpatterns = [
    path("tarefas/", criar_tarefa),
    path("tarefas/listar/", listar_tarefas),
    path(
        "tarefas/<int:pk>/atualizar-status/",
        atualizar_status,
    ),
    path("tarefas/<int:pk>/excluir/", excluir_tarefa),
    path("tarefas/relatorio/", relatorio_tarefas),
]
