from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .docs import (
    atualizar_status_schema,
    criar_tarefa_schema,
    excluir_tarefa_schema,
    listar_tarefas_schema,
    relatorio_tarefas_schema,
)
from .models import Tarefa
from .procedures import (
    adicionar_tarefa,
    atualizar_status_tarefa,
    gerar_relatorio_tarefas,
)
from .serializers import TarefaSerializer


@criar_tarefa_schema
@api_view(["POST"])
def criar_tarefa(request):
    descricao = request.data.get("descricao")
    status_tarefa = request.data.get("status")

    if not descricao or not status_tarefa:
        return Response(
            {"detail": "descrição e status são obrigatórios."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if status_tarefa not in ["pendente", "concluida"]:
        return Response(
            {"detail": 'Status inválido. O status deve ser "pendente" ou "concluida".'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        resultado = adicionar_tarefa(descricao, status_tarefa)
        if resultado:
            return Response(
                {
                    "detail": "Tarefa criada com sucesso",
                    "tarefa_id": resultado["tarefa_id"],
                    "descricao": resultado["descricao"],
                    "status": resultado["status"],
                    "data_criacao": resultado["data_criacao"],
                    "data_conclusao": resultado["data_conclusao"],
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            raise Exception("Erro ao obter os dados da tarefa.")
    except Exception as e:
        return Response(
            {"detail": f"Erro ao criar a tarefa: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@listar_tarefas_schema
@api_view(["GET"])
def listar_tarefas(request):
    if request.method == "GET":
        tarefas = Tarefa.objects.all()
        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data)


@atualizar_status_schema
@api_view(["PATCH"])
def atualizar_status(request, pk):
    try:
        novo_status = request.data.get("status")

        if not novo_status:
            return Response(
                {"detail": "O campo 'status' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        resultado = atualizar_status_tarefa(pk, novo_status)

        if "status" in resultado:
            return Response(
                {
                    "detail": "Status da tarefa atualizado com sucesso.",
                    "status": resultado["status"],
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": resultado["detail"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        print(f"Erro ao atualizar o status: {e}")
        return Response(
            {"detail": f"Erro interno no servidor: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@excluir_tarefa_schema
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


@relatorio_tarefas_schema
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
