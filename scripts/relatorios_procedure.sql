CREATE PROCEDURE sp_gerar_relatorio_tarefas
AS
BEGIN
    SET NOCOUNT ON;


    SELECT COUNT(*) AS quantidade_total_de_tarefas
    FROM tarefas_tarefa;

    SELECT 
        'quantidade concluida' AS descricao, COUNT(*) AS quantidade
    FROM tarefas_tarefa
    WHERE status COLLATE Latin1_General_CI_AI = 'concluida'

    UNION ALL

    SELECT 
        'quantidade pendente' AS descricao, COUNT(*) AS quantidade
    FROM tarefas_tarefa
    WHERE status COLLATE Latin1_General_CI_AI = 'pendente';

    SELECT 
        tarefa_id,
        descricao,
        status COLLATE Latin1_General_CI_AI AS status,
        data_criacao,
        data_conclusao
    FROM tarefas_tarefa
    WHERE status COLLATE Latin1_General_CI_AI IN ('concluida', 'pendente') 
    ORDER BY status, data_conclusao;
END;
