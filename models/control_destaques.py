from data.conexao import Conexao 

class Destaques:
    # O nome da função foi alterado para ser mais descritivo
    def buscar_todos_destaques():
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor(dictionary=True)

        # ADICIONADO: tcc.pdf_nome para funcionar no seu HTML
        sql = """
            SELECT 
                tcc.titulo,
                tcc.autor,
                tcc.descricao,
                tcc.data,
                tcc.pdf_nome, 
                tcc.palavrachave1,
                tcc.palavrachave2,
                tcc.palavrachave3,
                tcc.codigo AS tcc_codigo,
                orientador.nome_orientador,
                curso.nome_curso
            FROM 
                tbTcc AS tcc
            INNER JOIN 
                tbCurso AS curso ON tcc.cod_curso = curso.cod_curso
            INNER JOIN 
                tbTcc_Orientador AS tcc_orientador ON tcc.codigo = tcc_orientador.cod_tcc
            INNER JOIN 
                tbOrientador AS orientador ON tcc_orientador.cod_orientador = orientador.cod_orientador
            WHERE 
                tcc.destaque = 'sim';
        """
        cursor.execute(sql)

        # ALTERADO: de fetchone() para fetchall()
        # fetchall() retorna uma lista de todos os resultados.
        # Se não houver resultados, retorna uma lista vazia [], o que não quebra o loop.
        resultados = cursor.fetchall()

        conexao.close()
        return resultados