from data.conexao import Conexao


class Curso_orientador:
    def cadastro_curso(nome_curso):

        # Criando a conexão com o banco de dados
        conexao = Conexao.criar_conexao()

        # O cursor será responsável por manipular
        cursor = conexao.cursor()

        # Criando o sql que será executado
        sql = """INSERT INTO tbCurso
                    (nome_curso)
                VALUES
                    (%s)"""
               
        valores = (nome_curso)
   
        # Executando o comnado sql
        cursor.execute(sql,valores)
   
        # Confirmo a alteração (commit serve para fixar a alteração)
        conexao.commit()
   
        # Fecho a conexao com o banco
        cursor.close()
        conexao.close()

   
    def recuperar_curso():

        #Criar conexão
        conexao = Conexao.criar_conexao()

        # O cursor será responsável por manipular
        cursor = conexao.cursor(dictionary = True)

        # Criando o sql que será executado
        sql = "SELECT nome_curso FROM tbCurso;"

        #Executando o comando sql
        cursor.execute(sql)        

        #Recuperando os dados e jogando em uma varialvel
        resultado = cursor.fetchall()

        #Fecho a conexão (como não ouve alteração não preciso do commit)
        conexao.close()

        return resultado


    def cadastro_orientador(nome_orientador):

        # Criando a conexão com o banco de dados
        conexao = Conexao.criar_conexao()

        # O cursor será responsável por manipular
        cursor = conexao.cursor()

        # Criando o sql que será executado
        sql = """INSERT INTO tbOrientador
                    (nome_orientador)
                VALUES
                    (%s)"""
               
        valores = (nome_orientador)
   
        # Executando o comnado sql
        cursor.execute(sql,valores)
   
        # Confirmo a alteração (commit serve para fixar a alteração)
        conexao.commit()
   
        # Fecho a conexao com o banco
        cursor.close()
        conexao.close()



    def recuperar_orientador():

        #Criar conexão
        conexao = Conexao.criar_conexao()

        # O cursor será responsável por manipular
        cursor = conexao.cursor(dictionary = True)

        # Criando o sql que será executado
        sql = "SELECT nome_orientador FROM tbOrientadores;"

        #Executando o comando sql
        cursor.execute(sql)        

        #Recuperando os dados e jogando em uma varialvel
        resultado = cursor.fetchall()

        #Fecho a conexão (como não ouve alteração não preciso do commit)
        conexao.close()

        return resultado
