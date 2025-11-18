from data.conexao import Conexao


class Curso_orientador:
    # O '@staticmethod' indica que este método pertence à classe, mas não precisa de uma instância específica da classe para ser chamado (não usa 'self').
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
        valores = (nome_orientador, cod_curso)  
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
            sql = "SELECT nome_orientador, cod_orientador FROM tbOrientador where cod_curso = %s AND contratado = 1;"
            
            valores = (cod_curso,)

            #Executando o comando sql
            cursor.execute(sql, valores)        

            #Recuperando os dados e jogando em uma varialvel
            resultado = cursor.fetchall()

            #Fecho a conexão (como não ouve alteração não preciso do commit)
            conexao.close()

            return resultado

    def recuperar_todos_orientadores_com_status():
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor(dictionary=True)
        
        # Busca o orientador e o nome do curso para exibir na tabela
        sql = """
        SELECT 
            o.cod_orientador, 
            o.nome_orientador, 
            o.contratado, 
            c.nome_curso 
        FROM tbOrientador as o
        INNER JOIN tbCurso as c ON o.cod_curso = c.cod_curso
        ORDER BY o.nome_orientador;
        """
        
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conexao.close()
        return resultado

    def alterar_status_orientador(cod_orientador, novo_status):
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor()
        
        try:
            sql = "UPDATE tbOrientador SET contratado = %s WHERE cod_orientador = %s"
            valores = (novo_status, cod_orientador)
            cursor.execute(sql, valores)
            conexao.commit()
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao alterar status: {e}")
        finally:
            cursor.close()
            conexao.close()        


    @staticmethod
    def excluir_curso(cod_curso):
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor()
        try:
            # 1. Obter IDs dos orientadores deste curso (para o passo 2)
            sql_get_orientadores = "SELECT cod_orientador FROM tbOrientador WHERE cod_curso = %s"
            cursor.execute(sql_get_orientadores, (cod_curso,))
            # Usamos fetchall() e list comprehension para obter uma lista de IDs
            orientadores_ids = [row[0] for row in cursor.fetchall()]

            if orientadores_ids:
                # 2. Remover associações de TCCs com esses orientadores
                # Precisamos criar os placeholders (%s) dinamicamente para a cláusula IN
                format_strings = ','.join(['%s'] * len(orientadores_ids))
                sql_tcc_link = f"DELETE FROM tbTcc_Orientador WHERE cod_orientador IN ({format_strings})"
                cursor.execute(sql_tcc_link, tuple(orientadores_ids))
            
            # 3. Excluir os orientadores do curso
            sql_orientador = "DELETE FROM tbOrientador WHERE cod_curso = %s"
            cursor.execute(sql_orientador, (cod_curso,))
            
            # 4. Excluir o curso
            # ATENÇÃO: Isso VAI FALHAR se houver TCCs vinculados (tbTcc.cod_curso)
            # Isso é o comportamento DESEJADO (segurança). O try/except no app.py vai avisar o usuário.
            sql_curso = "DELETE FROM tbCurso WHERE cod_curso = %s"
            cursor.execute(sql_curso, (cod_curso,))
            
            conexao.commit()
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao excluir curso (ID: {cod_curso}): {e}")
            raise e # Re-lança a exceção para ser pega no app.py
        finally:
            cursor.close()
            conexao.close()