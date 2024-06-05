-- Cria a base de dados
CREATE DATABASE MinhaBaseDeDados;
GO

-- Seleciona a base de dados para usar
USE MinhaBaseDeDados;
GO

-- Cria uma tabela de exemplo
CREATE TABLE MinhaTabela (
    id INT PRIMARY KEY,
    nome NVARCHAR(100) NOT NULL
);
GO

-- Insere alguns dados de exemplo na tabela
INSERT INTO MinhaTabela (id, nome) VALUES (1, 'Exemplo1');
INSERT INTO MinhaTabela (id, nome) VALUES (2, 'Exemplo2');
INSERT INTO MinhaTabela (id, nome) VALUES (3, 'Exemplo3');
GO

-- Verifica se os dados foram inseridos
SELECT * FROM MinhaTabela;
GO
