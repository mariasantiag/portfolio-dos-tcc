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
                tbTcc.*,
                tbOrientador.nome_orientador,
                tbCurso.nome_curso
            FROM tbTcc
            INNER JOIN tbCurso 
                ON tbTcc.cod_curso = tbCurso.cod_curso
            INNER JOIN tbOrientador 
                ON tbOrientador.cod_curso = tbCurso.cod_curso
            ORDER BY tbTcc.data ASC;
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