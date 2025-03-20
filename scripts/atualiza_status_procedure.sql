CREATE PROCEDURE sp_atualizar_status_tarefa
    @tarefa_id INT,
    @novo_status VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM tarefas_tarefa WHERE tarefa_id = @tarefa_id)
    BEGIN
        RAISERROR('Tarefa não encontrada.', 16, 1);
        RETURN;
    END

    UPDATE tarefas_tarefa
    SET 
        status = @novo_status,
        data_conclusao = GETDATE()  
    WHERE tarefa_id = @tarefa_id;
END;
