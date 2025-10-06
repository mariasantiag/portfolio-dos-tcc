import os
import shutil
import mysql.connector
from data.conexao import Conexao

class Tcc:

    # Função para registrar as informações no banco de dados
    def registrar_tcc_no_banco(self, titulo, descricao, nome_pdf):
        try:
            # Criar conexão
            conexao = Conexao.criar_conexao()

            # O cursor será responsável por manipular
            cursor = conexao.cursor(dictionary=True)

            # Comandos SQL para inserir em diferentes tabelas
            sql_orientador = "INSERT INTO tbOrientador (nome_orientador) VALUES (%s)"
            sql_curso = "INSERT INTO tbCurso (nome_curso) VALUES (%s)"
            sql_tcc = """
                INSERT INTO tbTcc (titulo, autor, descricao, data, palavrachave1, palavrachave2, palavrachave3, destaques, pdf_nome) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Dados do TCC
            dados_tcc = (
                titulo, 'Autor do TCC', descricao, '2025-10-01',  # Data pode ser dinâmica
                'Palavra chave 1', 'Palavra chave 2', 'Palavra chave 3', 'Destaques do TCC', nome_pdf
            )

            # Inserindo os dados nas tabelas: tbOrientador, tbCurso e tbTcc
            cursor.execute(sql_orientador)
            cursor.execute(sql_curso)
            cursor.execute(sql_tcc, dados_tcc)

            # Commit para salvar todas as inserções no banco
            conexao.commit()

            print(f"TCC '{titulo}' registrado no banco de dados.")

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            conexao.rollback()  # Caso haja erro, desfazemos as inserções

        finally:
            cursor.close()
            conexao.close()

    # Função para salvar o PDF na pasta 'pdf' e registrar no banco de dados
    def salvar_tcc(self, titulo, descricao, pdf_path):

         # Criar conexão
        conexao = Conexao.criar_conexao()

        # O cursor será responsável por manipular
        cursor = conexao.cursor(dictionary=True)

        # Pasta onde os PDFs serão armazenados
        pasta_pdf = 'pdf'  # Assumindo que a pasta pdf já existe no seu projeto
        
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
        self.registrar_tcc_no_banco(titulo, descricao, nome_pdf)  # Usando 'self' para chamar o método
        
        print(f"TCC salvo com sucesso! PDF: {nome_pdf}")

        cursor.close()
        conexao.close()


# Caminho do arquivo PDF
pdf_path = '%s/%s/%s.pdf'