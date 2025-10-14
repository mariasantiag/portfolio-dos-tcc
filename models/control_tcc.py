import os
import shutil
import mysql.connector
from data.conexao import Conexao


class Tcc:

    def registrar_tcc_no_banco(self, titulo, autores, orientador, curso, descricao, data, chave1, chave2, chave3, destaque, pdf_nome):
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor(dictionary=True)

            sql_tcc = """
            INSERT INTO tbTcc (
                titulo, autor, cod_orientador, cod_curso, descricao, data,
                palavrachave1, palavrachave2, palavrachave3,
                destaque, pdf_nome
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """



            dados_tcc = (
                titulo, autores, orientador, curso, descricao, data,
                chave1, chave2, chave3,
                destaque, pdf_nome
            )

            cursor.execute(sql_tcc, dados_tcc)
            conexao.commit()

            print(f"TCC '{titulo}' registrado com sucesso.")

        except mysql.connector.Error as err:
            print(f"Erro ao registrar TCC: {err}")
            conexao.rollback()

        finally:
            cursor.close()
            conexao.close()

    def salvar_tcc(self, titulo, autores, orientador, curso, descricao, pdf_path, data, chave1, chave2, chave3, destaque):
        # Pasta onde os PDFs serão armazenados
        pasta_pdf = 'static/pdf'  # Assumindo que a pasta pdf já existe no seu projeto

        # Cria a pasta se não existir
        if not os.path.exists(pasta_pdf):
            os.makedirs(pasta_pdf)

        # Extrai o nome do arquivo PDF
        nome_pdf = os.path.basename(pdf_path)

        # Define o caminho completo para onde o PDF será movido
        caminho_pdf_destino = os.path.join(pasta_pdf, nome_pdf)

        # Move o PDF para a pasta 'pdf'
        shutil.copy(pdf_path, caminho_pdf_destino)

        # Agora, registra as informações no banco de dados (incluindo o nome do PDF)
        self.registrar_tcc_no_banco(titulo, autores, orientador, curso, descricao, data, chave1, chave2, chave3, destaque, nome_pdf)

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


