import mysql.connector
from data.conexao import Conexao

class Ano:
    def obter_tccs_por_data(self):
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor(dictionary=True)

            # SQL para buscar os TCCs e ordenar por data (assumindo que "data" é uma coluna do tipo DATE)
            sql_tccs = """
              SELECT
                    tcc.codigo,
                    tcc.titulo,
                    tcc.autor,
                    tcc.descricao,
                    DATE_FORMAT(data, '%d/%m/%Y') AS data_formatada_br,
                    curso.nome_curso,
                    tcc.pdf_nome,
                    -- A função GROUP_CONCAT junta os nomes dos orientadores em uma única string, separados por vírgula e espaço.
                    -- Damos a esta nova coluna o nome de 'orientadores'.
                    GROUP_CONCAT(orientador.nome_orientador SEPARATOR ', ') AS orientadores
                FROM
                    tbTcc AS tcc
				INNER JOIN
                    tbCurso AS curso ON tcc.cod_curso = curso.cod_curso
                --  Conecta Tcc (tcc) com Orientador (orientador) via a tabela de relacionamento (tto)
                INNER JOIN 
                    tbTcc_Orientador AS tto ON tcc.codigo = tto.cod_tcc
                INNER JOIN
                    tbOrientador AS orientador ON tto.cod_orientador = orientador.cod_orientador
                -- A cláusula GROUP BY é essencial. Ela agrupa todas as linhas que pertencem ao mesmo TCC em uma só.
                GROUP BY
                    tcc.codigo
                ORDER BY
                    data ASC;
            """  # DESC para obter os mais recentes primeiro

            cursor.execute(sql_tccs)
            tccs = cursor.fetchall()

            return tccs  # Retorna os TCCs ordenados por data

        except mysql.connector.Error as err:
            print(f"Erro ao buscar TCCs: {err}")
            return []

        finally:
            cursor.close()
            conexao.close()