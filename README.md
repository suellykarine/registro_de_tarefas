# Registro de Tarefas

Este projeto consiste em um sistema de registro de tarefas desenvolvido em Python com Django e SQL Server. O sistema permite cadastrar, listar, atualizar o status e excluir tarefas, além de gerar relatórios de tarefas concluídas e pendentes.

## Índice

- [Registro de Tarefas](#registro-de-tarefas)
  - [Índice](#índice)
  - [Instalação e Configuração](#instalação-e-configuração)
    - [Pré-requisitos](#pré-requisitos)
    - [Configuração do ambiente](#configuração-do-ambiente)
  - [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
  - [Procedimentos Armazenados](#procedimentos-armazenados)
    - [Adicionar Tarefa](#adicionar-tarefa)
    - [Atualizar Status de uma Tarefa](#atualizar-status-de-uma-tarefa)
    - [Gerar Relatório de Tarefas](#gerar-relatório-de-tarefas)
  - [Endpoints da API](#endpoints-da-api)
    - [Criar uma nova tarefa](#criar-uma-nova-tarefa)
    - [Listar todas as tarefas](#listar-todas-as-tarefas)
    - [Atualizar o status de uma tarefa](#atualizar-o-status-de-uma-tarefa)
    - [Excluir uma tarefa](#excluir-uma-tarefa)
    - [Gerar relatório de tarefas](#gerar-relatório-de-tarefas-1)
  - [Relatórios](#relatórios)
  - [Swagger e Documentação](#swagger-e-documentação)
  - [Tecnologias Utilizadas](#tecnologias-utilizadas)
    - [Autor](#autor)

## Instalação e Configuração

### Pré-requisitos

- Python 3.9+
- Django Rest Framework
- SQL Server
- Git
- Virtualenv

### Configuração do ambiente

1. Clone o repositório:
   ```sh
   git clone https://github.com/suellykarine/registro_de_tarefas.git
   cd registro_de_tarefas
   ```
2. Crie e ative um ambiente virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure o banco de dados SQLServer e rode os scripts SQL para criar e popular a tabela.

```sh
   DATABASE_URL=mssql://usuario:senha@servidor:porta/banco_de_dados
```

```sql
USE registro_de_tarefas;
GO


IF OBJECT_ID('dbo.tarefas_tarefa', 'U') IS NOT NULL
DROP TABLE dbo.tarefas_tarefa;
GO

CREATE TABLE dbo.tarefas_tarefa (
tarefa_id INT IDENTITY(1,1) PRIMARY KEY,
descricao VARCHAR(255) NOT NULL,
status VARCHAR(50) NOT NULL,
data_criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
data_conclusao DATETIME2 NULL
);
GO

INSERT INTO dbo.tarefas_tarefa (descricao, status, data_criacao, data_conclusao)
VALUES
('Estudar para o teste', 'pendente', GETDATE(), NULL),
('Fazer exercícios', 'concluída', GETDATE(), GETDATE()),
('Revisar código', 'concluída', GETDATE(), GETDATE()),
('Preparar documentação', 'pendente', GETDATE(), NULL),
('Enviar e-mail', 'concluída', GETDATE(), GETDATE());
GO
```

1. Aplique as migrações:

```sh
python manage.py makemigrations
python manage.py migrate
```

2. Execute o servidor:

```sh
python manage.py runserver
```

O servidor estará rodando em http://127.0.0.1:8000/

## Estrutura do Banco de Dados

A tabela `tarefas_tarefa` contém os seguintes campos:

- **tarefa_id** (`AutoField`): Identificador único da tarefa (chave primária).
- **descricao** (`CharField`): Descrição da tarefa (máximo de 255 caracteres).
- **status** (`CharField`): Status da tarefa (máximo de 50 caracteres).
- **data_criacao** (`DateTimeField`): Data e hora de criação da tarefa (automático).
- **data_conclusao** (`DateTimeField`): Data e hora de conclusão da tarefa (opcional).

## Procedimentos Armazenados

### Adicionar Tarefa

```sql
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

   
    IF @status NOT IN ('pendente', 'concluida') 
    BEGIN
        RAISERROR('Status inválido. O status deve ser "pendente" ou "concluida".', 16, 1);
        RETURN;
    END


    INSERT INTO dbo.tarefas_tarefa (descricao, status, data_criacao, data_conclusao)
    VALUES (@descricao, @status, GETDATE(), NULL);

    SET @nova_tarefa_id = SCOPE_IDENTITY();

    SELECT tarefa_id, descricao, status, data_criacao, data_conclusao
    FROM dbo.tarefas_tarefa
    WHERE tarefa_id = @nova_tarefa_id;
END;
GO


```

### Atualizar Status de uma Tarefa

```sql
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

    IF @novo_status NOT IN ('concluida', 'pendente')
    BEGIN
        RAISERROR('Status inválido. O status deve ser "concluida" ou "pendente".', 16, 1);
        RETURN;
    END

    UPDATE tarefas_tarefa
    SET 
        status = @novo_status,
        data_conclusao = CASE 
                            WHEN @novo_status = 'concluida' THEN GETDATE()
                            ELSE data_conclusao
                          END
    WHERE tarefa_id = @tarefa_id;


    SELECT @novo_status AS novo_status;
END;


```

### Gerar Relatório de Tarefas

```sql
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

```

## Endpoints da API

### Criar uma nova tarefa

`POST /tarefas/`

#### Descrição
Adiciona uma nova tarefa ao sistema.

#### Request Body
```json
{
  "descricao": "Estudar python",
  "status": "pendente"
}
```
Respostas:

201:
```json
{
  "detail": "Tarefa criada com sucesso",
  "tarefa_id": 35,
  "descricao": "Enviar relatório",
  "status": "pendente",
  "data_criacao": "2025-03-21T16:35:56.646666",
  "data_conclusao": null
}
```
400:
```http
{
  "detail": "descrição e status são obrigatórios."
}
```
500:
```http
{
  "detail": "Erro ao cadastrar uma tarefa"
}
```

### Listar todas as tarefas

`GET /tarefas/listar/`

#### Descrição
Listar todas as tarefas cadastradas.

Respostas

200 : 
```json
[
  {
    "tarefa_id": 1,
    "descricao": "Fazer compras",
    "status": "pendente",
    "data_criacao": "2025-03-21T12:00:00Z",
    "data_conclusao": null
  },
  {
    "tarefa_id": 2,
    "descricao": "Estudar",
    "status": "concluida",
    "data_criacao": "2025-03-21T12:00:00Z",
    "data_conclusao": "2025-03-22T12:00:00Z"
  }
]
```
500:
```http
{
  "detail": "Erro ao listar as tarefas"
}
```

### Atualizar o status de uma tarefa

`PATCH /tarefas/<int:pk>/atualizar-status/`

#### Descrição
Atualiza uma tarefa específica com base no ID (pk) fornecido.

#### Parâmetros
pk (obrigatório): ID da tarefa que será atualizada.

Respostas

200: 
```http
{
  "detail": "Status da tarefa atualizado com sucesso.",
  "status": "concluida"

```
400: 
```http
{
  "detail": "O campo 'status' é obrigatório."
}
```
404: 
```http
{
  "detail": "Tarefa não encontrada."
}
```
500:
```http
{
  "detail": "Erro ao atualizar uma tarefa"
}
```

### Excluir uma tarefa

`DELETE /tarefas/<int:pk>/excluir/`

#### Descrição
Exclui uma tarefa específica com base no ID (pk) fornecido.

#### Parâmetros
pk (obrigatório): ID da tarefa que será excluída.

Respostas

200 : 
```http
{
"detail": "Tarefa excluída com sucesso."
}
```
400: 
```http
{
  "detail": "Tarefa não encontrada."
}
```
500:
```http
{
  "detail": "Erro ao excluir a tarefa"
}
```

### Gerar relatório de tarefas

`GET /tarefas/relatorio/`

#### Descrição
Gera um relatório com o total de tarefas incluindo as pendentes e concluídas e seus respectivos detalhes.

Respostas

200 : 

```json
{
  "quantidade total de tarefas": 2,
  "tarefas concluidas": {
    "quantidade": 1,
    "tarefas": [
      {
        "tarefa_id": 3,
        "descricao": "Fazer exercício",
        "status": "concluida",
        "data_criacao": "2025-03-20T14:08:18.221414Z",
        "data_conclusao": "2025-03-21T16:00:31.086666Z"
      }
    ]
  },
  "tarefas pendentes": {
    "quantidade": 1,
    "tarefas": [
      {
        "tarefa_id": 5,
        "descricao": "Ir ao médico",
        "status": "pendente",
        "data_criacao": "2025-03-20T14:08:18.221414Z",
        "data_conclusao": null
      }
    ]
  }
}
```
500:
```http
{
  "detail": "Erro ao gerar relatório"
}
```

## Relatórios

O relatório de tarefas apresenta as seguintes informações:

```json
{
  "quantidade total de tarefas": 3,
  "tarefas concluidas": {
    "quantidade": 2,
    "tarefas": [
      {
        "tarefa_id": 3,
        "descricao": "Fazer exercício",
        "status": "concluida",
        "data_criacao": "2025-03-20T14:08:18.221414Z",
        "data_conclusao": "2025-03-21T16:00:31.086666Z"
      }
    ]
  },
  "tarefas pendentes": {
    "quantidade": 1,
    "tarefas": [
      {
        "tarefa_id": 5,
        "descricao": "Ir ao médico",
        "status": "pendente",
        "data_criacao": "2025-03-20T14:08:18.221414Z",
        "data_conclusao": null
      }
    ]
  }
}
```

## Swagger e Documentação

A documentação dos endpoints da API pode ser acessada pelo Swagger:

```
http://127.0.0.1:8000/api/docs/
```

## Tecnologias Utilizadas

- Python
- Django Rest Framework
- SQL Server
- Git

---

### Autor

Desenvolvido por [Suelly Araujo](https://github.com/suellykarine).
