
from data.conexao import Conexao
import mysql.connector

class Palavra:
    @staticmethod
    def pesquisar_palavra_chave(palavra_chave):
        # Conexão com o banco de dados
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor(dictionary=True)

        # SQL para buscar nas 3 colunas
        sql = """
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

        """

        
        palavra_qualquer = f"%{palavra_chave}%"  
        palavra_exata = f"{palavra_chave}"  
        cursor.execute(sql, (palavra_exata, palavra_exata, palavra_exata, palavra_exata, palavra_exata, palavra_exata, palavra_qualquer))

        # Retorna todos os resultados
        resultados = cursor.fetchall()

        # Fecha a conexão
        cursor.close()
        conexao.close()

        return resultados
