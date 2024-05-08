import pyodbc

server = r"tcp:mednat.ieeta.pt\SQLSERVER,8101"
db = "p5g1"
user = "p5g1"
psw = "!Admin12345"

connection = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={db};UID={user};PWD={psw};'

cnxn = pyodbc.connect(connection)

cursor = cnxn.cursor()
