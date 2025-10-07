from data.conexao import Conexao


class Curso_orientador:
    @staticmethod
    def cadastro_curso(nome_curso):
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor()

        sql = "INSERT INTO tbCurso (nome_curso) VALUES (%s)"
        valores = (nome_curso,)
        cursor.execute(sql, valores)

        conexao.commit()

        # Pega o id gerado do curso # PESQUISAR
        cod_curso = cursor.lastrowid

        cursor.close()
        conexao.close()

        return cod_curso  # Retorna o id para uso posterior


    @staticmethod
    def cadastro_orientador(nome_orientador, cod_curso):
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor()

        sql = "INSERT INTO tbOrientador (nome_orientador, cod_curso) VALUES (%s, %s)"
        valores = (nome_orientador, cod_curso)
        cursor.execute(sql, valores)

        conexao.commit()
        cursor.close()
        conexao.close()
