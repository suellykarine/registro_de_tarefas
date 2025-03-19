from django.urls import path

from . import views

urlpatterns = [
    path("tarefas/", views.criar_tarefa, name="criar_tarefa"),
]
