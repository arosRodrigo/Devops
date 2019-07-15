import pymysql

# Abrimos uma conexão com o banco de dados:
conexao = pymysql.connect(db='<nome do banco>', user='<usuário>', passwd='<senha>')

# Cria um cursor:
cursor = conexao.cursor()

# Executa o comando: <CRUD>
cursor.execute("insert into user(nome)value('manoel')")
    
# Efetua um commit no banco de dados.
# Por padrão, não é efetuado commit automaticamente. Você deve commitar para salvar
# suas alterações.
conexao.commit()
    
# Finaliza a conexão
conexao.close()
