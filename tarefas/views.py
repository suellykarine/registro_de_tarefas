from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Tarefa
from .serializers import TarefaSerializer


@api_view(["POST"])
def criar_tarefa(request):
    if request.method == "POST":
        serializer = TarefaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def listar_tarefas(request):
    if request.method == "GET":
        tarefas = Tarefa.objects.all()
        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data)


@api_view(["PATCH"])
def atualizar_status_tarefa(request, pk):
    try:
        tarefa = Tarefa.objects.get(pk=pk)
    except Tarefa.DoesNotExist:
        return Response(
            {"detail": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND
        )

    if "Status" not in request.data:
        return Response(
            {"detail": "Status não fornecido."}, status=status.HTTP_400_BAD_REQUEST
        )

    novo_status = request.data["Status"]

    if novo_status == "concluida":
        tarefa.DataConclusao = timezone.now()

    tarefa.Status = novo_status
    tarefa.save()

    serializer = TarefaSerializer(tarefa)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def excluir_tarefa(request, pk):
    try:
        tarefa = Tarefa.objects.get(pk=pk)
        tarefa.delete()
        return Response(
            {"detail": "Tarefa excluída com sucesso."},
            status=status.HTTP_204_NO_CONTENT,
        )
    except Tarefa.DoesNotExist:
        return Response(
            {"detail": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def relatorio_tarefas(request):
    tarefas_concluidas = Tarefa.objects.filter(Status="concluida")
    tarefas_pendentes = Tarefa.objects.filter(Status="Pendente")

    tarefas_concluidas_serializer = TarefaSerializer(tarefas_concluidas, many=True)
    tarefas_pendentes_serializer = TarefaSerializer(tarefas_pendentes, many=True)

    relatorio = {
        "tarefas_concluidas": {
            "quantidade": tarefas_concluidas.count(),
            "tarefas": tarefas_concluidas_serializer.data,
        },
        "tarefas_pendentes": {
            "quantidade": tarefas_pendentes.count(),
            "tarefas": tarefas_pendentes_serializer.data,
        },
    }

    return Response(relatorio, status=status.HTTP_200_OK)
