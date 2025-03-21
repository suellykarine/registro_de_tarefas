from django.db import connection


def adicionar_tarefa(descricao, status):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_adicionar_tarefa %s, %s", [descricao, status])
            nova_tarefa_id = cursor.fetchone()
            if nova_tarefa_id:
                return nova_tarefa_id[0]
            else:
                raise Exception("Erro ao obter o ID da tarefa.")
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
        return None


def atualizar_status_tarefa(tarefa_id, novo_status):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DECLARE @resultado INT; EXEC sp_atualizar_status_tarefa %s, %s, @resultado OUTPUT; SELECT @resultado;",
                [tarefa_id, novo_status],
            )
            resultado = cursor.fetchone()

            if resultado is None:
                return {"detail": "Erro ao atualizar o status da tarefa."}
            return {"detail": "Status atualizado com sucesso."}
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
