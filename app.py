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
    return render_template("principal.html")

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
    return render_template("cadastro-tcc.html")


@app.route("/paginaorientadorcurso")
def paginaorientadorcurso():
    return render_template("cadastro-curso-orientador.html")

@app.route("/post/cadastraorientadorcurso", methods= ["POST"])
def post_curso_orientador():
    # Peguei as informações vinda do usuário
    nome_curso = request.form.get("curso_nome")
    nome_orientador = request.form.get("orientador_nome")
   

    # Cadastrando a mensagem usando a classe mensagem
    Curso_orientador.cadastro_curso(nome_curso)
    Curso_orientador.cadastro_orientador(nome_orientador)
    
    # Redireciona para o index
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
    autores = request.form.get("autores")  # Pegando o valor de "autores"
    orientador = request.form.get("orientador")
    curso = request.form.get("curso")
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
    print("Arquivo existe?", os.path.exists(caminho_temporario))

    # Instanciando a classe Tcc
    tcc = Tcc()

    # Chama o método para registrar no banco de dados
    tcc.registrar_tcc_no_banco(
        titulo=titulo,
        autores=autores,
        orientador=orientador,
        curso=curso,
        descricao=descricao,
        data=data,
        chave1=chave1,
        chave2=chave2,
        chave3=chave3,
        destaque=destaque,
        pdf_nome=pdf.filename
    )

    # Chama o método para salvar o PDF na pasta 'pdf'
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