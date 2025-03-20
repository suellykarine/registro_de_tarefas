from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Tarefa
from .procedures import (
    adicionar_tarefa,
    atualizar_status_tarefa,
    gerar_relatorio_tarefas,
)
from .serializers import TarefaSerializer


@api_view(["POST"])
def criar_tarefa(request):
    descricao = request.data.get("descricao")
    status_tarefa = request.data.get("status")

    if not descricao or not status_tarefa:
        return Response(
            {"detail": "descrição e status são obrigatórios."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        with connection.cursor() as cursor:
            nova_tarefa_id = None
            cursor.execute(
                "DECLARE @nova_tarefa_id INT; EXEC sp_adicionar_tarefa %s, %s, @nova_tarefa_id OUTPUT; SELECT @nova_tarefa_id;",
                [descricao, status_tarefa],
            )
            nova_tarefa_id = cursor.fetchone()[0]
        return Response(
            {"detail": "Tarefa criada com sucesso", "tarefa_id": nova_tarefa_id},
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response(
            {"detail": f"Erro ao criar a tarefa: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def listar_tarefas(request):
    if request.method == "GET":
        tarefas = Tarefa.objects.all()
        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data)


@api_view(["PATCH"])
def atualizar_status(request, pk):
    try:
        novo_status = request.data.get("status")

        if not novo_status:
            return Response(
                {"detail": "O campo 'status' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with connection.cursor() as cursor:
            cursor.execute(
                "EXEC sp_atualizar_status_tarefa %s, %s;",
                [pk, novo_status],
            )

        return Response(
            {"detail": "Status da tarefa atualizado com sucesso."},
            status=status.HTTP_200_OK,
        )

    except Exception as e:

        print(f"Erro ao atualizar o status: {e}")
        return Response(
            {"detail": f"Erro interno no servidor: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["DELETE"])
def excluir_tarefa(request, pk):
    try:
        tarefa = Tarefa.objects.get(pk=pk)
        tarefa.delete()
        return Response(
            {"detail": "Tarefa excluída com sucesso."},
            status=status.HTTP_200_OK,
        )
    except Tarefa.DoesNotExist:
        return Response(
            {"detail": "Tarefa não encontrada."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def relatorio_tarefas(request):
    try:
        relatorio = gerar_relatorio_tarefas()
        return Response(relatorio, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return Response(
            {"detail": f"Erro ao gerar relatório: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
