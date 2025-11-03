# models/control_historico.py

from data.conexao import Conexao
import mysql.connector

class Historico:

    def registrar_acao(usuario_nome, acao, detalhes):
        """
        Registra uma nova ação no histórico.
        Ex: registrar_acao("Admin Zé", "Adicionou TCC", "TCC: 'O Impacto...'")
        """
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor()

            sql = """
                INSERT INTO tbHistorico (usuario_nome, acao, detalhes)
                VALUES (%s, %s, %s)
            """
            valores = (usuario_nome, acao, detalhes)
            
            cursor.execute(sql, valores)
            conexao.commit()

        except mysql.connector.Error as err:
            print(f"Erro ao registrar histórico: {err}")
            conexao.rollback()
        finally:
                cursor.close()
                conexao.close()

    def recuperar_historico():
        """
        Recupera todos os registros do histórico, do mais novo para o mais antigo.
        """
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor(dictionary=True) # dictionary=True é essencial

            sql = "SELECT * FROM tbHistorico ORDER BY data_hora DESC"
            
            cursor.execute(sql)
            logs = cursor.fetchall()
            return logs

        except mysql.connector.Error as err:
            print(f"Erro ao recuperar histórico: {err}")
            return [] # Retorna lista vazia em caso de erro
        finally:
                cursor.close()
                conexao.close()

    def limpar_historico():
        """
        Deleta TODOS os registros da tabela de histórico.
        """
        try:
            conexao = Conexao.criar_conexao()
            cursor = conexao.cursor()

            # TRUNCATE TABLE é mais rápido que DELETE FROM e reseta o auto-increment
            sql = "TRUNCATE TABLE tbHistorico;"
            
            cursor.execute(sql)
            conexao.commit()
            print("Histórico limpo com sucesso.")

        except mysql.connector.Error as err:
            print(f"Erro ao limpar histórico: {err}")
            conexao.rollback()
        finally:
                cursor.close()
                conexao.close()