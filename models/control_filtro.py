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
                tcc.data,
                tcc.pdf_nome,
                curso.nome_curso,
                -- Agrupa os nomes dos orientadores selecionados para este TCC
                GROUP_CONCAT(orientador.nome_orientador SEPARATOR ', ') AS nome_orientadores
            FROM 
                tbTcc AS tcc
            INNER JOIN 
                tbCurso AS curso ON tcc.cod_curso = curso.cod_curso
            -- Faz o JOIN com a tabela de relacionamento TCC-Orientador
            INNER JOIN 
                tbTcc_Orientador AS tccorientador ON tcc.codigo = tccorientador.cod_tcc
            -- Pega o nome do orientador
            INNER JOIN
                tbOrientador AS orientador ON tccorientador.cod_orientador = orientador.cod_orientador
            -- Agrupa todas as linhas que pertencem ao mesmo TCC em uma só
            GROUP BY 
                tcc.codigo
            -- Ordena pela data do TCC (ASC para mais antigos primeiro, como você pediu)
            ORDER BY 
                tcc.data ASC;
                
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