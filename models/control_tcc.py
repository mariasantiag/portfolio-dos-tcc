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

        # Executa o mesmo comando SQL várias vezes, uma para cada conjunto de dados que você fornece.
        cursor.executemany(sql_relacao, dados_relacao)


    def registrar_tcc_no_banco(self, titulo, autores, orientadores_ids, curso, descricao, data, chave1, chave2, chave3, chave4, chave5, destaque, pdf_nome):
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor(dictionary=True)

            # INSERE O TCC NA tbTcc (sem o cod_orientador)
            sql_tcc = """
            INSERT INTO tbTcc (
                titulo, autor, cod_curso, descricao, data,
                palavrachave1, palavrachave2, palavrachave3, palavrachave4, palavrachave5,
                destaque, pdf_nome
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            dados_tcc = (
                titulo, autores, curso, descricao, data,
                chave1, chave2, chave3, chave4, chave5,
                destaque, pdf_nome
            )

            cursor.execute(sql_tcc, dados_tcc)
            tcc_id = cursor.lastrowid  # Pega o ID do TCC recém-inserido

            # INSERE OS ORIENTADORES NA tbTcc_Orientador
            self.registrar_orientadores_no_banco(tcc_id, orientadores_ids, conexao, cursor)

            # Efetiva (salva permanentemente) todas as exclusões feitas.
            conexao.commit()
            print(f"TCC '{titulo}' e seus orientadores registrados com sucesso.")

        except mysql.connector.Error as err:
            print(f"Erro ao registrar TCC: {err}")
            # Se a operação de salvar o TCC envolve múltiplas etapas e o erro acontece no meio do caminho, o `rollback()` desfaz TODAS as
            # alterações feitas até aquele ponto. Isso garante que o banco de dados não fique em um estado
            # inconsistente (com dados "pela metade"). É um mecanismo de segurança essencial.
            conexao.rollback()

        finally:
            # Garante que o cursor e a conexão sejam fechados mesmo com erro
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conexao' in locals() and conexao is not None:
                conexao.close()


    def salvar_tcc(self, titulo, autores, orientadores_ids, curso, descricao, pdf_path, data, chave1, chave2, chave3,chave4, chave5, destaque):
        # Define o nome da pasta onde os arquivos PDF serão guardados.
        pasta_pdf = 'static/pdf'
        # Verifica se a pasta chamada 'pdf' já existe no diretório do projeto.
        if not os.path.exists(pasta_pdf):
             # Se a pasta não existir, este comando a cria.
             os.makedirs(pasta_pdf)

        # Pega apenas o nome do arquivo do caminho completo fornecido.
        # Exemplo: se pdf_path for 'C:/Downloads/meu_trabalho.pdf', nome_pdf será 'meu_trabalho.pdf'.
        nome_pdf = os.path.basename(pdf_path)

        # Cria o caminho completo onde o arquivo PDF será salvo.Junta o nome da pasta ('pdf') com o nome do arquivo ('meu_trabalho.pdf'),
        # resultando em um caminho como 'pdf/meu_trabalho.pdf'.
        caminho_pdf_destino = os.path.join(pasta_pdf, nome_pdf)
       
        # shutil.move para mover o arquivo temporário (melhor do que copy e remove depois)
        shutil.move(pdf_path, caminho_pdf_destino)

        # Agora, registra as informações no banco de dados (incluindo o nome do PDF)
        # Passa a lista de IDs: orientadores_ids
        self.registrar_tcc_no_banco(titulo, autores, orientadores_ids, curso, descricao, data, chave1, chave2, chave3, chave4, chave5, destaque, nome_pdf)

        print(f"TCC salvo com sucesso! PDF: {nome_pdf}")


    def exibi_tcc():
        conexao = None # Inicializa a conexão como None
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor(dictionary=True)

            # SQL modificado para agrupar os orientadores por TCC
            sql_tcc = """
                SELECT
                    tcc.codigo,
                    tcc.titulo,
                    tcc.autor,
                    tcc.descricao,
                    tcc.data,
                    curso.nome_curso,
                    tcc.pdf_nome,
                    -- A função GROUP_CONCAT junta os nomes dos orientadores em uma única string, separados por vírgula e espaço.
                    -- Damos a esta nova coluna o nome de 'orientadores'.
                    GROUP_CONCAT(orientador.nome_orientador SEPARATOR ', ') AS orientadores
                FROM
                    tbTcc AS tcc
                INNER JOIN
                    tbCurso AS curso ON tcc.cod_curso = curso.cod_curso
                INNER JOIN 
                    tbOrientador AS orientador ON curso.cod_curso = orientador.cod_curso
                -- A cláusula GROUP BY é essencial. Ela agrupa todas as linhas que pertencem ao mesmo TCC em uma só.
                GROUP BY
                    tcc.codigo
                ORDER BY
                    tcc.data DESC;
            """

            # Executa um único comando SQL de cada vez.
            cursor.execute(sql_tcc)
            
            # Recuperando os dados e guardando em uma variavel
            trabalhos = cursor.fetchall()

            return trabalhos
        
        except Exception as e: 
            print(f"Erro ao buscar TCCs: {e}")
            if conexao:
                conexao.rollback()
            return [] # Retorna uma lista vazia em caso de erro

        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()



    def deletar_tcc(codigo):
       
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor(dictionary=True) # Usar dictionary=True para fetchone
        titulo_deletado = None # Inicializa o título

        try:
            #  Busca o título ANTES de deletar
            sql_busca = "SELECT titulo FROM tbTcc WHERE codigo = %s;"
            cursor.execute(sql_busca, (codigo,))
            resultado = cursor.fetchone()
            if resultado:
                # Guarda na variável
                titulo_deletado = resultado['titulo']

            # Agora que as ligações foram removidas, define o comando para apagar o registro principal do TCC na tabela `tbTcc` (a tabela "pai").
            sql_filho = "DELETE FROM tbTcc_Orientador WHERE cod_tcc = %s;"
            valores = (codigo,) 
            cursor.execute(sql_filho, valores)

            #  Deletar da tabela "pai" tbTcc
            sql_pai = "DELETE FROM tbTcc WHERE codigo = %s;"
            cursor.execute(sql_pai, valores)

            # Efetiva (salva permanentemente) todas as exclusões feitas. Sem o `commit()`, nada seria realmente apagado no banco de dados.
            conexao.commit()
            print(f"TCC com código {codigo} deletado com sucesso.")

        except Exception as e:
            conexao.rollback()
            print(f"Ocorreu um erro ao deletar o TCC: {e}")
            titulo_deletado = None # Garante que não retorne um título se falhar

        finally:
            cursor.close()
            conexao.close()
            
        # Retorna o título que conseguimos buscar
        return titulo_deletado
    
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