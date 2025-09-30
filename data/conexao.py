import mysql.connector

class Conexao:
    
    def criar_conexao():
        # Criando a conexão com o banco de dados
        conexao = mysql.connector.connect(host = "localhost",
                                        port = 3306,
                                        user = "root",
                                        password = "root",
                                        database = "dbTcc")
        
    

        return conexao