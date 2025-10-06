from flask import Flask, render_template, request, redirect
import datetime
import mysql.connector
from models.control_tcc import Tcc
from models.control_curso_orientador import Curso_orientador
from models.control_destaques import Destaques
from models.control_recentes import Recentes
from models.control_usuario_admin import Usuario

from flask import session
app = Flask(__name__)
app.secret_key = "seila2"

@app.route("/")
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

@app.route("/paginainicial")
def paginaprincipal():
    return render_template("principal.html")

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

app.run(debug=True)