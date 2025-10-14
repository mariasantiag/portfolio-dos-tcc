from flask import Flask, render_template, request, redirect
import datetime
import mysql.connector
import os
import shutil
from models.control_tcc import Tcc
from models.control_curso_orientador import Curso_orientador
from models.control_destaques import Destaques
from models.control_recentes import Recentes
from models.control_usuario_admin import Usuario
from models.control_palavra_chave import Palavra

from flask import jsonify, request

from flask import session
app = Flask(__name__)
app.secret_key = "seila2"

@app.route("/")
@app.route("/paginainicial")
def paginaprincipal():
    
    tccs = Tcc.exibi_tcc()
    rec_tccs = Tcc.recuperar_tcc()
    # Atualize a chamada para a nova função
    destaques = Destaques.buscar_todos_destaques()

    return render_template("principal.html", tccs=tccs, rec_tccs=rec_tccs, destaques=destaques)

@app.route("/paginalogin")
def paginalogin():
    return render_template("login.html")  

@app.route("/paginacadastro")
def paginacadastro():
    return render_template("cadastro.html")  


@app.route("/post/cadastrarusuario", methods= ["POST"])
def post_usuario():
    # Peguei as informações vinda do usuário
    nome = request.form.get("nome")
    login  = request.form.get("login")
    senha = request.form.get("senha")

    # Cadastrando a mensagem usando a classe mensagem
    Usuario.cadastro_usuario(nome, login, senha)
   
    # Redireciona para o index
    return redirect("/paginalogin")

@app.route("/paginacadastrotcc")
def paginacadastrotcc():
    curso = Curso_orientador.recuperar_curso()  
    return render_template("cadastro-tcc.html", curso=curso)


@app.route("/api/orientadores/<int:cod_curso>")
def api_orientadores(cod_curso):
    orientadores = Curso_orientador.recuperar_orientador(cod_curso)
    # Exemplo de retorno esperado
    # orientadores = [
    #    {"id": 1, "nome_orientador": "Fulano"},
    #    {"id": 2, "nome_orientador": "Beltrano"},
    # ]
    return jsonify(orientadores)


@app.route("/paginaorientadorcurso")
def paginaorientadorcurso():
    return render_template("cadastro-curso-orientador.html")

@app.route("/post/cadastraorientadorcurso", methods=["POST"])
def post_curso_orientador():
    nome_curso = request.form.get("curso_nome")
    orientadores = request.form.getlist("orientador_nome")  # Lista de orientadores
    orientadores = request.form.getlist("orientador_nome")  # Lista de orientadores

    # Cadastra o curso e pega o ID
    cod_curso = Curso_orientador.cadastro_curso(nome_curso)

    # Insere cada orientador individualmente
    for nome_orientador in orientadores:
        if nome_orientador.strip():
            Curso_orientador.cadastro_orientador(nome_orientador.strip(), cod_curso)

    return redirect("/paginainicial")

@app.route("/post/logar", methods=["POST"])
def post_logar():
    login = request.form.get("login")
    senha = request.form.get("senha")
   
    esta_logado = Usuario.logar(login, senha)

    if esta_logado:
        return redirect("/paginainicial")
    else:
        return redirect("/paginalogin")
   
@app.route("/deslogar")
def deslogar():
    session.clear()
    return redirect("/")

# Mantenha o import os e o from flask import request, redirect
# Adicione: import os

# ... (código anterior) ...

# ... (código anterior) ...

@app.route("/post/cadastrar/tcc", methods=["POST"])
def post_tcc():
    # Pegando todas as informações do formulário
    titulo = request.form.get("titulo")
    autores = request.form.get("autores")
    curso = int(request.form.get("curso"))
    orientadores_ids = request.form.getlist("orientador[]") # ou "orientador"
    descricao = request.form.get("descricao")
    data = request.form.get("data")
    chave1 = request.form.get("chave1")
    chave2 = request.form.get("chave2")
    chave3 = request.form.get("chave3")
    destaque = request.form.get("destaque")
    pdf = request.files.get("pdf")

    # Verifica se o arquivo PDF foi enviado
    if not pdf or pdf.filename == "":
        return "Nenhum arquivo PDF enviado", 400

    # Criar diretório temporário caso não exista
    if not os.path.exists("uploads_tmp"):
        os.makedirs("uploads_tmp")

    # Definindo o caminho temporário para salvar o PDF
    caminho_temporario = os.path.join("uploads_tmp", pdf.filename)
    pdf.save(caminho_temporario)

    print(f"Arquivo salvo temporariamente em: {caminho_temporario}")

    # Instanciando a classe Tcc
    tcc = Tcc()

    # Chama o método completo que salva o PDF e registra no banco
    tcc.salvar_tcc(
        titulo, autores, orientadores_ids, curso, descricao, caminho_temporario,
        data, chave1, chave2, chave3, destaque
    )

    # Remove o arquivo temporário após a cópia
    if os.path.exists(caminho_temporario):
        os.remove(caminho_temporario)

    # Redireciona para a página inicial após o cadastro
    return redirect("/paginainicial")

@app.route("/apagartcc/<codigo>")
def apagartcc(codigo):
    Tcc.deletar_tcc(codigo)
    return redirect("/paginainicial") 

@app.route("/pesquisar", methods=['GET'])
def pesquisar():
    # Captura o valor da palavra chave para pesquisa
    palavra_chave = request.args.get('pesquisa_palavra_chave')

    # Chama a função de pesquisa
    resultados = Palavra.pesquisar_palavra_chave(palavra_chave)

    # Retorna os resultados para o template
    return render_template('principal.html', tccs=resultados)

if __name__ == '__main__':
    app.run(debug=True)


app.run(debug=True)