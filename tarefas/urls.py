from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
