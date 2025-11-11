from flask import Flask, render_template, request, redirect, flash
import os
from models.control_tcc import Tcc
from models.control_curso_orientador import Curso_orientador
from models.control_destaques import Destaques
from models.control_usuario_admin import Usuario
from models.control_filtro import Ano
from models.control_palavra_chave import Palavra
from models.control_historico import Historico 
import random

from flask import jsonify, request

from flask import session
app = Flask(__name__)
app.secret_key = "seila2"

# Caminho para rota principal 
@app.route("/")
@app.route("/paginainicial")
def paginaprincipal():
    
    tccs = Tcc.exibi_tcc()
    
    # Busca todos os destaques
    todos_destaques = Destaques.buscar_todos_destaques()

    # Define quantos destaques você quer sortear
    num_destaques_desejados = 2

    # Usa random.sample para selecionar 'k' itens aleatórios
    #  Verificamos o tamanho da lista para evitar erros se houver menos de 2 destaques
    if len(todos_destaques) > num_destaques_desejados:
        destaques_selecionados = random.sample(todos_destaques, num_destaques_desejados)
    else:
        # Se houver 2 ou menos destaques, use todos eles
        destaques_selecionados = todos_destaques

    
    return render_template("principal.html", tccs=tccs, destaques=destaques_selecionados)

# Caminho para pagina de login 
@app.route("/paginalogin")
def paginalogin():
    return render_template("login.html")  

# Caminho da página de histórico
@app.route("/paginahistorico")
def paginahistorico():
    logs = Historico.recuperar_historico()
    return render_template("historico.html", logs=logs)

# Caminho para limpar o histórico
@app.route("/historico/limpar")
def limpar_historico_route():
    try:
        # Chama a função do control
        Historico.limpar_historico()
        # Mensagem que vai aparecer quando apertar em excluir se for "success"
    except Exception as e:
        print(f"Erro ao limpar o histórico: {e}", "danger")
    
    # Redireciona de volta para a página de histórico
    return redirect("/paginahistorico")

# Caminho para pagina de cadastro do admin
@app.route("/paginacadastro")
def paginacadastro():
    return render_template("cadastro.html")  

# Caminho para pagina de verificação do admin 
@app.route("/paginaverificacao")
def paginaverificacao():
    return render_template("verificacao.html")

# Caminho que verifica se o codigo inserido pelo admin é valido 
@app.route("/post/verificarcodigo", methods=["POST"])
def verificarcodigo():
    senha = "admin"
    codigo = request.form.get("codigo")

    if senha == codigo:
        return redirect("/paginacadastro")
    else:
        return redirect("/paginaverificacao")

# Caminho que cadastra o admin
@app.route("/post/cadastrarusuario", methods= ["POST"])
def post_usuario():
 
    # Peguei as informações vinda do usuário
    nome = request.form.get("nome")
    login  = request.form.get("login")
    senha = request.form.get("senha")
    
    # Validação: se a senha for menor que 8
    if len(senha) < 8:
        flash("A senha deve ter pelo menos 8 caracteres.", "error")
        return redirect("/paginacadastro")

    # Cadastrando a mensagem usando a classe mensagem
    Usuario.cadastro_usuario(nome, login, senha)
    
    flash("Cadastro efetuado com sucesso!", "success")
    # Redireciona para o index
    
    return redirect("/paginacadastro")

# Caminho para pagina de cadastro de tcc 
@app.route("/paginacadastrotcc")
def paginacadastrotcc():
    if 'usuario' not in session:
        return redirect("/paginalogin")
    curso = Curso_orientador.recuperar_curso()  
    return render_template("cadastro-tcc.html", curso=curso)

# Caminho para para pagina de cadastro de orientador e curso 
@app.route("/paginaorientadorcurso")
def paginaorientadorcurso(): 
    if 'usuario' not in session:
        return redirect("/paginalogin")     
    curso = Curso_orientador.recuperar_curso()  

    return render_template("cadastro-curso-orientador.html", curso=curso)

@app.route("/post/excluirorientadorcurso", methods=["POST"])
def post_excluir_orientador_curso():
    cod_orientador = request.form.get("orientador_delete")
    cod_curso = request.form.get("curso_delete")

    try:
        if cod_orientador:
            # Prioriza excluir o orientador se ele foi selecionado
            Curso_orientador.excluir_orientador(cod_orientador)
            flash("Orientador excluído com sucesso.")
        
        elif cod_curso:
            # Se NENHUM orientador foi selecionado, mas um curso foi...
            # ...interpretamos como exclusão do CURSO.
            Curso_orientador.excluir_curso(cod_curso)
            flash("Curso e seus orientadores associados foram excluídos com sucesso.")
        
        else:
            flash("Nenhuma seleção válida para exclusão.")
    
    except Exception as e:
        print(f"Erro ao excluir: {e}")
        # Captura erros de FK (Foreign Key)
        if "foreign key constraint" in str(e).lower():
             flash("Erro: Não é possível excluir. Este curso está vinculado a um ou mais TCCs.")
        else:
             flash(f"Erro ao excluir: {e}")

    return redirect("/paginaorientadorcurso")


@app.route("/api/orientadores/<int:cod_curso>")
def api_orientadores(cod_curso):
    orientadores = Curso_orientador.recuperar_orientador(cod_curso)
    # Exemplo de retorno esperado
    # orientadores = [
    #    {"id": 1, "nome_orientador": "Fulano"},
    #    {"id": 2, "nome_orientador": "Beltrano"},
    # ]
    return jsonify(orientadores)

# Cadastra o orientador e o curso 
@app.route("/post/cadastraorientadorcurso", methods=["POST"])
def post_curso_orientador():
    if 'usuario' not in session:
        return redirect("/paginalogin")
    nome_curso = request.form.get("curso_nome")
    orientadores = request.form.getlist("orientador_nome")  # Lista de orientadores

    try:
        # Cadastra o curso e pega o ID
        cod_curso = Curso_orientador.cadastro_curso(nome_curso)

        # Insere cada orientador individualmente
        for nome_orientador in orientadores:
            if nome_orientador.strip():
                Curso_orientador.cadastro_orientador(nome_orientador.strip(), cod_curso)
        if nome_curso == '':
            flash("Erro ao cadastrar curso e orientadores. Verifique os dados e tente novamente.", "error")
            Curso_orientador.cadastro_curso()
            Curso_orientador.cadastro_orientador()
            return  redirect("/paginaorientadorcurso")
        if orientadores == '':
            flash("Erro ao cadastrar curso e orientadores. Verifique os dados e tente novamente.", "error")
            Curso_orientador.cadastro_curso()
            Curso_orientador.cadastro_orientador()
            return  redirect("/paginaorientadorcurso")
        flash("Curso e orientadores cadastrados com sucesso!", "success")

    except Exception as e:
        print(f"Erro ao cadastrar curso e orientadores: {e}")
        flash("Erro ao cadastrar curso e orientadores. Verifique os dados e tente novamente.", "error")

    return redirect("/paginaorientadorcurso")

# Verifica se o admin está logado 
@app.route("/post/logar", methods=["POST"])
def post_logar():
    login = request.form.get("login")
    senha = request.form.get("senha")
    
    esta_logado = Usuario.logar(login, senha)

    if esta_logado:
        return redirect("/paginainicial")
    else:
        flash("Login ou senha incorretos. Tente novamente.", "error")
        return redirect("/paginalogin")

# Rota para logoff  
@app.route("/deslogar")
def deslogar():
    session.clear()
    return redirect("/")

#  Cadastro de TCC
@app.route("/post/cadastrar/tcc", methods=["POST"])
def post_tcc():
    if 'usuario' not in session:
        return redirect("/paginalogin")
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
    chave4 = request.form.get("chave4")
    chave5 = request.form.get("chave5")
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

    
    try:
    # Instanciando a classe Tcc
        tcc = Tcc()

        # Chama o método completo que salva o PDF e registra no banco
        tcc.salvar_tcc(
            titulo, autores, orientadores_ids, curso, descricao, caminho_temporario,
            data, chave1, chave2, chave3, chave4, chave5, destaque
        )
        flash("TCC cadastrado com sucesso!", "success")
    except Exception as e:
        flash("Erro ao cadastrar tcc!", "error")
        
        

    # Historico 
    try:
        # Pega o nome do admin logado na sessão (que foi salvo no login)
        nome_admin = session.get('nome_usuario', 'Admin Desconhecido')
        
        # Registra a ação no histórico
        Historico.registrar_acao(
            usuario_nome=nome_admin,
            acao="Adicionou TCC",
            detalhes=f"TCC: '{titulo}'"
        )
    except Exception as e:
        print(f"Erro ao salvar log de cadastro: {e}")
        # O TCC foi salvo, mas o histórico(log) falhou. Não quebra a aplicação.
  

    # Remove o arquivo temporário após a cópia
    if os.path.exists(caminho_temporario):
        os.remove(caminho_temporario)

    # Redireciona para a página inicial após o cadastro
    
    return redirect("/paginacadastrotcc")

# Excluir TCC
@app.route("/apagartcc/<codigo>")
def apagartcc(codigo):
    if 'usuario' not in session:
        return redirect("/paginalogin")
    # Chama a função deletar_tcc
    titulo_deletado = Tcc.deletar_tcc(codigo)

    if titulo_deletado: # Se o TCC foi deletado com sucesso
        try:
            # pega o nome do usuario ou admin desconhecido (caso não reconheça o usuário)
            nome_admin = session.get('nome_usuario', 'Admin Desconhecido')
            
            # Cadastra o tcc excluido no histórico
            Historico.registrar_acao(
                usuario_nome=nome_admin,
                acao="Excluiu TCC",
                detalhes=f"TCC: '{titulo_deletado}'"
            )
        # erro, caso não de para salvar
        except Exception as e:
            print(f"Erro ao salvar log de exclusão: {e}")
  

    return redirect("/paginainicial") 

# Pesquisa por palavra chave, titulo e autores do tcc 
@app.route("/pesquisar", methods=['GET'])
def pesquisar():
    # Captura o valor da palavra chave para pesquisa
    palavra_chave = request.args.get('pesquisa_palavra_chave')

    # Chama a função de pesquisa
    resultados = Palavra.pesquisar_palavra_chave(palavra_chave)

    # Retorna os resultados para o template
    return render_template('principal.html', tccs=resultados)

# Organiza TCC pela Data de conclusão 
@app.route("/tccs_por_data")
def tccs_por_data():
    tcc_controller = Ano()
    tccs_ordenados = tcc_controller.obter_tccs_por_data()
    return render_template('ano.html', tccs_ordenados=tccs_ordenados)


if __name__ == '__main__':
    app.run(debug=True)