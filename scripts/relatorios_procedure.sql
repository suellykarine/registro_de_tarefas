CREATE PROCEDURE sp_gerar_relatorio_tarefas
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        'Quantidade de Tarefas Concluídas' AS descricao,
        COUNT(*) AS quantidade
    FROM tarefas_tarefa
    WHERE status COLLATE Latin1_General_CI_AI = 'concluida' 

    UNION ALL

    SELECT 
        'Quantidade de Tarefas Pendentes' AS descricao,
        COUNT(*) AS quantidade
    FROM tarefas_tarefa
    WHERE status COLLATE Latin1_General_CI_AI = 'pendente' 
    SELECT 
        tarefa_id,
        descricao,
        status,
        data_conclusao
    FROM tarefas_tarefa
    WHERE status COLLATE Latin1_General_CI_AI IN ('concluida', 'pendente') 
    ORDER BY status, data_conclusao;
END;
