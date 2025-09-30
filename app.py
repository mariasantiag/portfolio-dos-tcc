from flask import Flask, render_template, request, redirect
import datetime
import mysql.connector
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
    email  = request.form.get("email")
    senha = request.form.get("senha")

    # Cadastrando a mensagem usando a classe mensagem
    Usuario.cadastro_usuario(nome, email, senha)
    
    # Redireciona para o index
    return redirect("/paginalogin")

# @app.route("/post/logar", methods=["POST"])
# def post_logar():
#     email = request.form.get("email")
#     senha = request.form.get("senha")
    
#     esta_logado = Usuario.logar(email, senha)

#     if esta_logado:
#         return redirect("/paginainicial")
#     else:
#         return redirect("/paginalogin")
    
# @app.route("/deslogar")
# def deslogar():
#     session.clear()
#     return redirect("/") 

app.run(debug=True)