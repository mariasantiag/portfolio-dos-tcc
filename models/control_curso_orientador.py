from data.conexao import Conexao


class Curso_orientador:
    @staticmethod
    def cadastro_curso(nome_curso):
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor()

        sql = "INSERT INTO tbCurso (nome_curso) VALUES (%s)"
        valores = (nome_curso,)
        cursor.execute(sql, valores)

        conexao.commit()

        # Pega o id gerado do curso # PESQUISAR
        cod_curso = cursor.lastrowid

        cursor.close()
        conexao.close()

        return cod_curso  # Retorna o id para uso posterior

    @staticmethod
    def cadastro_orientador(nome_orientador, cod_curso):
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor()

        sql = "INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES (%s, %s)"
        valores = (nome_orientador, cod_curso)  # <- nome_orientador é string
        cursor.execute(sql, valores)

        conexao.commit()
        cursor.close()
        conexao.close()



    def recuperar_curso():

            #Criar conexão
            conexao = Conexao.criar_conexao()

            # O cursor será responsável por manipular
            cursor = conexao.cursor(dictionary = True)

            # Criando o sql que será executado
            sql = "SELECT nome_curso, cod_curso FROM tbCurso;"

            #Executando o comando sql
            cursor.execute(sql)        

            #Recuperando os dados e jogando em uma varialvel
            resultado = cursor.fetchall()

            #Fecho a conexão (como não ouve alteração não preciso do commit)
            conexao.close()

            return resultado



    
    def recuperar_orientador(cod_curso):

            #Criar conexão
            conexao = Conexao.criar_conexao()

            # O cursor será responsável por manipular
            cursor = conexao.cursor(dictionary = True)

            # Criando o sql que será executado
            sql = "SELECT nome_orientador, cod_orientador FROM tbOrientador where cod_curso = %s;"

            valores = (cod_curso,)

            #Executando o comando sql
            cursor.execute(sql, valores)        

            #Recuperando os dados e jogando em uma varialvel
            resultado = cursor.fetchall()

            #Fecho a conexão (como não ouve alteração não preciso do commit)
            conexao.close()

            return resultado
    
