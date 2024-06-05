import pyodbc

# Parâmetros de conexão
server = 'JOAOPINTO' # Substitua pelo seu servidor
database = 'MinhaBaseDeDados' # Nome da base de dados que acabamos de criar
username = 'sa'
password = os.getenv("SQL_PASSWORD")
cnxn_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Conectar ao banco de dados
cnxn = pyodbc.connect(cnxn_string)
cursor = cnxn.cursor()

# # Dados a serem inseridos
# # Certifique-se de que a tabela e as colunas correspondem ao esquema de sua base de dados
# dados_a_inserir = [(4, 'Nome4'), (5, 'Nome5'), (6, 'Nome6')]

# # Preparar e executar a instrução SQL de inserção
# instrucao_sql = 'INSERT INTO MinhaTabela (id, nome) VALUES (?, ?)'
# for dado in dados_a_inserir:
#     cursor.execute(instrucao_sql, dado)

# # Commitar as inserções e fechar a conexão
# cnxn.commit()
# cursor.close()
# cnxn.close()

# print("Dados inseridos com sucesso.")
