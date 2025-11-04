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
                    tbTcc.titulo,
                    tbTcc.autor,
                    tbTcc.descricao,
                    tbTcc.data,
                    tbCurso.nome_curso,
                    tbTcc.cod_curso,
                    tbTcc.codigo,
                    tbTcc.pdf_nome,
                    GROUP_CONCAT(orientador.nome_orientador SEPARATOR ', ') AS orientadores
                FROM
                    tbTcc
                INNER JOIN
                    tbCurso ON tbTcc.cod_curso = tbCurso.cod_curso
                INNER JOIN
                    tbTcc_Orientador AS tccorientador ON tbTcc.codigo = tccorientador.cod_tcc

                INNER JOIN
                    tbOrientador AS orientador ON tccorientador.cod_orientador = orientador.cod_orientador
                WHERE
                    palavrachave1 LIKE %s OR palavrachave2 LIKE %s OR palavrachave3 LIKE %s OR palavrachave4 LIKE %s OR palavrachave5 LIKE %s OR titulo LIKE %s OR autor LIKE %s
                GROUP BY
                    tbTcc.codigo, -- Use a chave primária do TCC aqui para agrupar corretamente
                    tbTcc.titulo,
                    tbTcc.autor,
                    tbTcc.descricao,
                    tbTcc.data,
                    tbCurso.nome_curso,
                    tbTcc.cod_curso,
                    tbTcc.pdf_nome;
                
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