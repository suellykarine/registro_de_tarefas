from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

criar_tarefa_schema = extend_schema(
    summary="Criar uma nova tarefa",
    description="Adiciona uma nova tarefa ao sistema.",
    request={
        "application/json": {"example": {"descricao": "string", "status": "string"}}
    },
    responses={
        201: OpenApiResponse(
            response=inline_serializer(
                name="CriarTarefaResponse",
                fields={
                    "detail": serializers.CharField(),
                    "tarefa_id": serializers.IntegerField(),
                },
            ),
            examples=[
                OpenApiExample(
                    "Tarefa criada com sucesso",
                    value={"detail": "Tarefa criada com sucesso", "tarefa_id": 1},
                    response_only=True,
                ),
            ],
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name="ErroValidacao",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Erro de validação",
                    value={"detail": "descrição e status são obrigatórios."},
                    response_only=True,
                ),
            ],
        ),
        500: OpenApiResponse(
            response=inline_serializer(
                name="ErroInterno",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Erro interno no servidor",
                    value={"detail": "Erro ao criar a tarefa"},
                    response_only=True,
                ),
            ],
        ),
    },
)

listar_tarefas_schema = extend_schema(
    summary="Listar tarefas",
    description="Lista as tarefas cadastradas.",
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="ListarTarefaResponse",
                fields={
                    "id": serializers.IntegerField(),
                    "descricao": serializers.CharField(),
                    "status": serializers.CharField(),
                    "data_criacao": serializers.DateTimeField(),
                    "data_conclusao": serializers.DateTimeField(allow_null=True),
                },
            ),
            examples=[
                OpenApiExample(
                    "Lista de tarefas",
                    value=[
                        {
                            "id": 1,
                            "descricao": "Fazer compras",
                            "status": "pendente",
                            "data_criacao": "2025-03-21T10:00:00Z",
                            "data_conclusao": None,
                        },
                        {
                            "id": 2,
                            "descricao": "Enviar relatório",
                            "status": "concluído",
                            "data_criacao": "2025-03-20T14:30:00Z",
                            "data_conclusao": "2025-03-21T16:06:35.160000Z",
                        },
                    ],
                    response_only=True,
                ),
            ],
        ),
        500: OpenApiResponse(
            response=inline_serializer(
                name="ErroInterno",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Erro interno no servidor",
                    value={"detail": "Erro ao listar as tarefas"},
                    response_only=True,
                ),
            ],
        ),
    },
)

atualizar_status_schema = extend_schema(
    summary="Atualizar o status de uma tarefa",
    description="Modifica o status de uma tarefa específica informando o ID na URL.",
    parameters=[
        OpenApiParameter(
            name="id",
            description="ID da tarefa a ser atualizada",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
    ],
    request=inline_serializer(
        name="AtualizarStatusTarefa",
        fields={
            "status": serializers.CharField(required=True),
        },
    ),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="AtualizarStatusResponse",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Status atualizado com sucesso",
                    value={"detail": "Status da tarefa atualizado com sucesso."},
                    response_only=True,
                ),
            ],
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name="ErroValidacaoResponse",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Erro de validação",
                    value={"detail": "O campo 'status' é obrigatório."},
                    response_only=True,
                ),
            ],
        ),
        404: OpenApiResponse(
            response=inline_serializer(
                name="TarefaNaoEncontradaResponse",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Tarefa não encontrada",
                    value={"detail": "Tarefa não encontrada."},
                    response_only=True,
                ),
            ],
        ),
        500: OpenApiResponse(
            response=inline_serializer(
                name="ErroInternoResponse",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Erro interno no servidor",
                    value={"detail": "Erro ao atualizar o status da tarefa"},
                    response_only=True,
                ),
            ],
        ),
    },
)


excluir_tarefa_schema = extend_schema(
    summary="Excluir uma tarefa",
    description="Remove uma tarefa com base no ID informado na URL.",
    parameters=[
        OpenApiParameter(
            name="id",
            description="ID da tarefa a ser excluída",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="ExcluirTarefaResponse",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Tarefa excluída com sucesso",
                    value={"detail": "Tarefa excluída com sucesso."},
                    response_only=True,
                ),
            ],
        ),
        404: OpenApiResponse(
            response=inline_serializer(
                name="TarefaNaoEncontradaResponse",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Tarefa não encontrada",
                    value={"detail": "Tarefa não encontrada."},
                    response_only=True,
                ),
            ],
        ),
        500: OpenApiResponse(
            response=inline_serializer(
                name="ErroInternoResponse",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Erro interno no servidor",
                    value={"detail": "Erro ao excluir a tarefa"},
                    response_only=True,
                ),
            ],
        ),
    },
)

relatorio_tarefas_schema = extend_schema(
    summary="Gerar relatório de tarefas",
    description="Gera um relatório com o total de tarefas incluindo as pendentes e concluídas e seus respectivos detalhes.",
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="RelatorioTarefasResponse",
                fields={
                    "concluidas": serializers.DictField(
                        child=serializers.ListField(
                            child=serializers.DictField(child=serializers.CharField())
                        )
                    ),
                    "pendentes": serializers.DictField(
                        child=serializers.ListField(
                            child=serializers.DictField(child=serializers.CharField())
                        )
                    ),
                },
            ),
            examples=[
                OpenApiExample(
                    "Relatório de tarefas",
                    value={
                        "quantidade total de tarefas": 3,
                        "tarefas concluidas": {
                            "quantidade": 2,
                            "tarefas": [
                                {
                                    "tarefa_id": 3,
                                    "descricao": "Fazer exercício",
                                    "status": "concluida",
                                    "data_criacao": "2025-03-20T14:08:18.221414Z",
                                    "data_conclusao": "2025-03-21T16:00:31.086666Z",
                                },
                                {
                                    "tarefa_id": 4,
                                    "descricao": "Entregar relatório",
                                    "status": "concluida",
                                    "data_criacao": "2025-03-20T14:08:18.221414Z",
                                    "data_conclusao": "2025-03-21T16:00:31.086666Z",
                                },
                            ],
                        },
                        "tarefas pendentes": {
                            "quantidade": 1,
                            "tarefas": [
                                {
                                    "tarefa_id": 5,
                                    "descricao": "Ir ao médico",
                                    "status": "pendente",
                                    "data_criacao": "2025-03-20T14:08:18.221414Z",
                                    "data_conclusao": None,
                                }
                            ],
                        },
                    },
                    response_only=True,
                ),
            ],
        ),
        500: OpenApiResponse(
            response=inline_serializer(
                name="ErroInternoRelatorioResponse",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    "Erro ao gerar relatório",
                    value={"detail": "Erro ao gerar relatório"},
                    response_only=True,
                ),
            ],
        ),
    },
)
