
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
                            titulo,
                            autor,
                            descricao,
                            data,
                            nome_curso,
                            nome_orientador as orientadores
                        FROM
                            tbTcc
                        INNER JOIN
                            tbCurso ON tbTcc.cod_curso = tbCurso.cod_curso
                        inner join 
                            tborientador as orientador on tbcurso.cod_curso = orientador.cod_curso
					  WHERE palavrachave1 LIKE %s OR palavrachave2 LIKE %s OR palavrachave3 LIKE %s  ;

        """

        
        palavra = f"%{palavra_chave}%"  
        cursor.execute(sql, (palavra, palavra, palavra))

        # Retorna todos os resultados
        resultados = cursor.fetchall()

        # Fecha a conexão
        cursor.close()
        conexao.close()

        return resultados
