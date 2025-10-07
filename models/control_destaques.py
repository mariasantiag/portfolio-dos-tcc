from data.conexao import Conexao 

class Destaques:
    def ultima_mensagem():
            #Criar conexão 
            conexao = Conexao.criar_conexao()

            # O cursor será responsável por manipular
            cursor = conexao.cursor(dictionary = True)

            # Criando o sql que será executado
            sql = """  SELECT 
                            tcc.titulo,
                            tcc.autor,
                            tcc.descricao,
                            tcc.data,
                            tcc.palavrachave1,
                            tcc.palavrachave2,
                            tcc.palavrachave3,
                            tcc.codigo AS tcc_codigo,
                            orientador.nome AS orientador_nome,
                            curso.nome AS curso_nome
                        FROM 
                            tbTcc tcc
                        INNER JOIN 
                            tbOrientador orientador ON tcc.cod_orientador = orientador.cod_orientador
                        INNER JOIN 
                            tbCurso curso ON tcc.cod_curso = curso.cod_curso
                        WHERE 
                            tcc.destaque = 'sim';"""

            #Executando o comando sql
            cursor.execute(sql)        

            #Recuperando os dados e jogando em uma varialvel 
            resultado = cursor.fetchone()

            #Fecho a conexão (como não ouve alteração não preciso do commit)
            conexao.close()

            return resultado