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


from flask import session
app = Flask(__name__)
app.secret_key = "seila2"

@app.route("/")
@app.route("/paginainicial")
def paginaprincipal():
    
    tccs = Tcc.exibi_tcc()
    selecao= Tcc.visualiza_tcc()


    return render_template("principal.html", tccs = tccs, selecao = selecao)

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
    orientador = Curso_orientador.recuperar_orientador()
    return render_template("cadastro-tcc.html", curso=curso, orientador=orientador)

@app.route("/paginaorientadorcurso")
def paginaorientadorcurso():
    return render_template("cadastro-curso-orientador.html")

@app.route("/post/cadastraorientadorcurso", methods=["POST"])
def post_curso_orientador():
    nome_curso = request.form.get("curso_nome")
    nome_orientador = request.form.get("orientador_nome")

    # 1. Cadastrar curso e pegar id
    cod_curso = Curso_orientador.cadastro_curso(nome_curso)

    # 2. Cadastrar orientador já vinculando ao curso
    Curso_orientador.cadastro_orientador(nome_orientador, cod_curso)

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

@app.route("/post/cadastrar/tcc", methods=["POST"])
def post_tcc():
    # Pegando todas as informações do formulário
    titulo = request.form.get("titulo")
    autores = request.form.get("autores")
    curso = int(request.form.get("curso"))
    orientador = int(request.form.get("orientador"))
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
        titulo, autores, orientador, curso, descricao, caminho_temporario, 
        data, chave1, chave2, chave3, destaque
    )

    # Remove o arquivo temporário após a cópia
    if os.path.exists(caminho_temporario):
        os.remove(caminho_temporario)

    # Redireciona para a página inicial após o cadastro
    return redirect("/paginainicial")



app.run(debug=True)