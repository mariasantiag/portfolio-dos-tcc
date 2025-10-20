from data.conexao import Conexao 

class Destaques:
    # O nome da função foi alterado para ser mais descritivo
    def buscar_todos_destaques():
        conexao = None
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor(dictionary=True)

            # SQL modificado para agrupar orientadores
            sql = """
                SELECT 
                    tcc.codigo AS tcc_codigo,
                    tcc.titulo,
                    tcc.autor,
                    tcc.descricao,
                    tcc.data,
                    tcc.pdf_nome, 
                    tcc.palavrachave1,
                    tcc.palavrachave2,
                    tcc.palavrachave3,
                    curso.nome_curso,
                    -- Agrupa os nomes dos orientadores em uma única string chamada 'orientadores'
                    GROUP_CONCAT(orientador.nome_orientador SEPARATOR ', ') AS orientadores
                FROM 
                    tbTcc AS tcc
                INNER JOIN 
                    tbCurso AS curso ON tcc.cod_curso = curso.cod_curso
                INNER JOIN 
                    tbTcc_Orientador AS tcc_orientador ON tcc.codigo = tcc_orientador.cod_tcc
                INNER JOIN 
                    tbOrientador AS orientador ON tcc_orientador.cod_orientador = orientador.cod_orientador
                WHERE 
                    tcc.destaque = 'sim'
                -- Agrupa o resultado por código do TCC para ter uma linha por trabalho
                GROUP BY
                    tcc.codigo;
            """
            # Executa um único comando SQL de cada vez.
            cursor.execute(sql)

            # Recuperando os dados e guardando em uma variavel
            resultados = cursor.fetchall()
            
            return resultados

        except Exception as e:
            print(f"Erro ao buscar destaques: {e}")
            return [] # Retorna lista vazia em caso de erro

        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()