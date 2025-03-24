USE registro_de_tarefas;
GO

IF OBJECT_ID('dbo.tarefas_tarefa', 'U') IS NOT NULL
    DROP TABLE dbo.tarefas_tarefa;
GO

CREATE TABLE dbo.tarefas_tarefa (
    tarefa_id INT IDENTITY(1,1) PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pendente', 'concluida')),
    data_criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    data_conclusao DATETIME2 NULL
);
GO

INSERT INTO dbo.tarefas_tarefa (descricao, status, data_criacao, data_conclusao)
VALUES
    ('Estudar para o teste', 'pendente', GETDATE(), NULL),
    ('Fazer exercícios', 'concluida', GETDATE(), GETDATE()),
    ('Revisar código', 'concluida', GETDATE(), GETDATE()),
    ('Preparar documentação', 'pendente', GETDATE(), NULL),
    ('Enviar e-mail', 'concluida', GETDATE(), GETDATE());
GO
