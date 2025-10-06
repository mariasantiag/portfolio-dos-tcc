# from flask import Flask, render_template, request, redirect
# import datetime
# import mysql.connector
# import os
# import shutil
# from models.control_tcc import Tcc
# from models.control_curso_orientador import Curso_orientador
# from models.control_destaques import Destaques
# from models.control_recentes import Recentes
# from models.control_usuario_admin import Usuario

# from flask import session
# app = Flask(__name__)
# app.secret_key = "seila2"

# @app.route("/")
# @app.route("/paginainicial")
# def paginaprincipal():
#     return render_template("principal.html")

# @app.route("/paginalogin")
# def paginalogin():
#     return render_template("login.html")   

# @app.route("/paginacadastro")
# def paginacadastro():
#     return render_template("cadastro.html")   


# @app.route("/post/cadastrarusuario", methods= ["POST"])
# def post_usuario():
#     # Peguei as informações vinda do usuário
#     nome = request.form.get("nome")
#     login  = request.form.get("login")
#     senha = request.form.get("senha")

#     # Cadastrando a mensagem usando a classe mensagem
#     Usuario.cadastro_usuario(nome, login, senha)
    
#     # Redireciona para o index
#     return redirect("/paginalogin")

# @app.route("/paginacadastrotcc")
# def paginacadastrotcc():
#     return render_template("cadastro-tcc.html")


# @app.route("/paginaorientadorcurso")
# def paginaorientadorcurso():
#     return render_template("cadastro-curso-orientador.html")

# @app.route("/post/logar", methods=["POST"])
# def post_logar():
#     login = request.form.get("login")
#     senha = request.form.get("senha")
    
#     esta_logado = Usuario.logar(login, senha)

#     if esta_logado:
#         return redirect("/paginainicial")
#     else:
#         return redirect("/paginalogin")
    
# @app.route("/deslogar")
# def deslogar():
#     session.clear()
#     return redirect("/") 

# # @app.route("/post/cadastrar/tcc", methods=["POST"])
# # def post_tcc():
# #     titulo = request.form.get("titulo")
# #     autores = request.form.get("autores")
# #     orientador = request.form.get("orientador")
# #     curso = request.form.get("curso")
# #     data = request.form.get("data")
# #     descricao = request.form.get("descricao")
# #     destaque = request.form.get("destaque")
# #     chave1= request.form.get("chave1")
# #     chave2= request.form.get("chave2")
# #     chave3= request.form.get("chave3")

# #     # Arquivo PDF enviado
# #     pdf = request.files.get("pdf")

# #     if not pdf:
# #         return "Nenhum arquivo PDF enviado", 400

# #     # Salva temporariamente para depois mover
# #     caminho_temporario = os.path.join("uploads_tmp", pdf.filename)
# #     pdf.save(caminho_temporario)

# #     # Criar instância da classe Tcc
# #     tcc = Tcc()

# #     # Chamar método de salvar
# #     tcc.salvar_tcc(titulo, descricao, caminho_temporario)

# #     return redirect("/paginainicial")


# @app.route("/post/cadastrar/tcc", methods=["POST"])
# def post_tcc():
#     titulo = request.form.get("titulo")
#     descricao = request.form.get("descricao")
#     pdf = request.files.get("pdf")

#     if not pdf or pdf.filename == "":
#         return "Nenhum arquivo PDF enviado", 400

#     if not os.path.exists("uploads_tmp"):
#         os.makedirs("uploads_tmp")

#     caminho_temporario = os.path.join("uploads_tmp", pdf.filename)
#     pdf.save(caminho_temporario)

#     print(f"Arquivo salvo temporariamente em: {caminho_temporario}")
#     print("Arquivo existe?", os.path.exists(caminho_temporario))

#     tcc = Tcc()
#     tcc.registrar_tcc_no_banco(titulo, descricao, pdf)
#     tcc.salvar_tcc(titulo, descricao, caminho_temporario)

#     # Remove arquivo temporário após cópia
#     if os.path.exists(caminho_temporario):
#         os.remove(caminho_temporario)

#     return redirect("/paginainicial")


# app.run(debug=True)