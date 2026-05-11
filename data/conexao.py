import mysql.connector

class Conexao:
    
    # def criar_conexao():
    #     # Criando a conexão com o banco de dados
    #     conexao = mysql.connector.connect(host = "localhost",
    #                                     port = 3306,
    #                                     user = "root",
    #                                     password = "root",
    #                                     database = "dbTcc")

    #     return conexao

    def criar_conexao():
        conexao = mysql.connector.connect(
                        host = "bibliotccabd.mysql.database.azure.com",
                        user = "BiblioTcca_admin",
                        password = "@admin-SENAI-!2025",
                        database = "dbTcc"
        )

        return conexao
    
