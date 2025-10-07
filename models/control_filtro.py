import mysql.connector
from data.conexao import Conexao

class Ano:
    def obter_tccs_por_data(self):
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor(dictionary=True)

            # SQL para buscar os TCCs e ordenar por data (assumindo que "data" é uma coluna do tipo DATE)
            sql_tccs = """
            SELECT * FROM tbTcc
            ORDER BY data DESC
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