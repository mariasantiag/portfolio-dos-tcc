import os
import shutil
import mysql.connector
from data.conexao import Conexao


# ... (imports no topo)

class Tcc:

    def registrar_orientadores_no_banco(self, tcc_id, orientadores_ids, conexao, cursor):
        """Salva a lista de orientadores na tabela tbTcc_Orientador."""
        if not orientadores_ids:
            return

        sql_relacao = "INSERT INTO tbTcc_Orientador (cod_tcc, cod_orientador) VALUES (%s, %s)"
       
        # Cria uma lista de tuplas (tcc_id, orientador_id) para execução em massa
        dados_relacao = [(tcc_id, int(o_id)) for o_id in orientadores_ids]

        cursor.executemany(sql_relacao, dados_relacao)


    def registrar_tcc_no_banco(self, titulo, autores, orientadores_ids, curso, descricao, data, chave1, chave2, chave3, destaque, pdf_nome):
        # NOTA: orientadores_ids é agora uma LISTA
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor(dictionary=True)

            # 1. INSERE O TCC NA tbTcc (sem o cod_orientador)
            sql_tcc = """
            INSERT INTO tbTcc (
                titulo, autor, cod_curso, descricao, data,
                palavrachave1, palavrachave2, palavrachave3,
                destaque, pdf_nome
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            dados_tcc = (
                titulo, autores, curso, descricao, data,
                chave1, chave2, chave3,
                destaque, pdf_nome
            )

            cursor.execute(sql_tcc, dados_tcc)
            tcc_id = cursor.lastrowid  # Pega o ID do TCC recém-inserido

            # 2. INSERE OS ORIENTADORES NA tbTcc_Orientador
            self.registrar_orientadores_no_banco(tcc_id, orientadores_ids, conexao, cursor)

            conexao.commit()
            print(f"TCC '{titulo}' e seus orientadores registrados com sucesso.")

        except mysql.connector.Error as err:
            print(f"Erro ao registrar TCC: {err}")
            conexao.rollback()

        finally:
            # Garante que o cursor e a conexão sejam fechados mesmo com erro
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conexao' in locals() and conexao is not None:
                conexao.close()

    def salvar_tcc(self, titulo, autores, orientador, curso, descricao, pdf_path, data, chave1, chave2, chave3, destaque):
        # Pasta onde os PDFs serão armazenados
        pasta_pdf = 'static/pdf'  # Assumindo que a pasta pdf já existe no seu projeto

    def salvar_tcc(self, titulo, autores, orientadores_ids, curso, descricao, pdf_path, data, chave1, chave2, chave3, destaque):
        # ... (código de salvamento do PDF permanece igual) ...
        pasta_pdf = 'pdf'
        if not os.path.exists(pasta_pdf):
             os.makedirs(pasta_pdf)

        nome_pdf = os.path.basename(pdf_path)
        caminho_pdf_destino = os.path.join(pasta_pdf, nome_pdf)
       
        # Usa shutil.move para mover o arquivo temporário (melhor do que copy e remove depois)
        shutil.move(pdf_path, caminho_pdf_destino)

        # Agora, registra as informações no banco de dados (incluindo o nome do PDF)
        # Passa a lista de IDs: orientadores_ids
        self.registrar_tcc_no_banco(titulo, autores, orientadores_ids, curso, descricao, data, chave1, chave2, chave3, destaque, nome_pdf)

        print(f"TCC salvo com sucesso! PDF: {nome_pdf}")

    def exibi_tcc():
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor(dictionary=True)

            sql_tcc="""
                        SELECT
                            codigo,
                            titulo,
                            autor,
                            descricao,
                            data,
                            nome_curso,
                            nome_orientador,
                            pdf_nome
                        FROM
                            tbTcc
                        INNER JOIN
                            tbCurso ON tbTcc.cod_curso = tbCurso.cod_curso
                        inner join 
                            tborientador on tbcurso.cod_curso = tborientador.cod_curso;

                        
            """


            cursor.execute(sql_tcc)
            
            trabalhos=cursor.fetchall()

            return trabalhos
        
        except:
            print("Nenhum TCC encontrado")
            conexao.rollback()

        finally:
            cursor.close()
            conexao.close()


    def deletar_tcc(codigo):
         # Criando a conexão com o banco de dados
        conexao = Conexao.criar_conexao()

        # O cursor será responsável por manipular
        cursor = conexao.cursor()

        # Criando o sql que será executado
        sql = """DELETE from tbTcc WHERE codigo = %s;"""
                   
        valores = (codigo,)
       
        # Executando o comnado sql
        cursor.execute(sql,valores)
       
        # Confirmo a alteração, SERVE PAR FIXAR ALTERAÇÃO, SE ALTEROU, EXCLUIU OU FEZ UPDATE, OU SEJA SERVE PARA CONFIRMAR ALTERAÇÃO
        conexao.commit()
       
        # Fecho a conexao com o banco
        cursor.close()
        conexao.close() 

    
    def recuperar_tcc():
     
        # Criando a conexão com o banco de dados
        conexao = Conexao.criar_conexao()

        # O cursor será responsável por manipular
        cursor = conexao.cursor(dictionary= True)

         # Criando o sql que será executado
        sql = "SELECT * FROM  tbTcc; "
                   
        # Executando o comnado sql
        cursor.execute(sql)
       
        # Recuperando os dados e guardando em uma variavel
        resultado = cursor.fetchall()
       
        # Fecho a conexao com o banco
        conexao.close()

        return resultado