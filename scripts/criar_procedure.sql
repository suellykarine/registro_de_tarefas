USE registro_de_tarefas;
GO

IF OBJECT_ID('dbo.sp_adicionar_tarefa', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_adicionar_tarefa;
GO

CREATE PROCEDURE dbo.sp_adicionar_tarefa
    @descricao NVARCHAR(255),
    @status NVARCHAR(50),
    @nova_tarefa_id INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.tarefas_tarefa (descricao, status, data_criacao)
    VALUES (@descricao, @status, GETDATE());

    SET @nova_tarefa_id = SCOPE_IDENTITY();
END;
GO