from django.db import connection


def adicionar_tarefa(descricao, status):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DECLARE @nova_tarefa_id INT;
                EXEC sp_adicionar_tarefa %s, %s, @nova_tarefa_id OUTPUT;
                SELECT tarefa_id, descricao, status, data_criacao, data_conclusao
                FROM dbo.tarefas_tarefa WHERE tarefa_id = @nova_tarefa_id;
                """,
                [descricao, status],
            )
            resultado = cursor.fetchone()
            if resultado:
                return {
                    "tarefa_id": resultado[0],
                    "descricao": resultado[1],
                    "status": resultado[2],
                    "data_criacao": resultado[3],
                    "data_conclusao": resultado[4],
                }
            else:
                raise Exception("Erro ao obter os dados da tarefa.")
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
        return None


def atualizar_status_tarefa(tarefa_id, novo_status):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "EXEC sp_atualizar_status_tarefa %s, %s;",
                [tarefa_id, novo_status],
            )
            resultado = cursor.fetchone()

            if resultado:
                return {
                    "status": resultado[0],
                }
            else:
                return {"detail": "Erro ao atualizar o status da tarefa."}
    except Exception as e:
        return {"detail": f"Erro ao atualizar status: {str(e)}"}


def gerar_relatorio_tarefas():
    with connection.cursor() as cursor:
        cursor.execute("EXEC sp_gerar_relatorio_tarefas")

        resultado_total = cursor.fetchall()
        cursor.nextset()
        resultado_contagem = cursor.fetchall()
        cursor.nextset()
        resultado_detalhes = cursor.fetchall()

    relatorio = {
        "quantidade total de tarefas": resultado_total[0][0] if resultado_total else 0,
        "tarefas concluidas": {"quantidade": 0, "tarefas": []},
        "tarefas pendentes": {"quantidade": 0, "tarefas": []},
    }

    for row in resultado_contagem:
        categoria = row[0].strip().lower()
        if "concluída" in categoria or "concluida" in categoria:
            relatorio["tarefas concluidas"]["quantidade"] = row[1]
        elif "pendente" in categoria:
            relatorio["tarefas pendentes"]["quantidade"] = row[1]

    for row in resultado_detalhes:
        tarefa = {
            "tarefa_id": row[0],
            "descricao": row[1],
            "status": row[2].strip().lower(),
            "data_criacao": row[3],
            "data_conclusao": row[4],
        }
        if tarefa["status"] in ["concluída", "concluida"]:
            relatorio["tarefas concluidas"]["tarefas"].append(tarefa)
        elif tarefa["status"] == "pendente":
            relatorio["tarefas pendentes"]["tarefas"].append(tarefa)

    return relatorio
