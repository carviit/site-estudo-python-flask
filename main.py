from flask import Flask, get_flashed_messages, render_template, redirect, request, flash, send_from_directory
import json
import ast
import os

logado = False

app = Flask(__name__)
app.config['SECRET_KEY'] =  'CARLOS'

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():

    if logado == True:

        with open('usuarios.json', 'r') as usuariosTemp:
            usuarios = json.load(usuariosTemp)

        return render_template("administrador.html", usuarios = usuarios)
    if logado == False:
        return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    
    global logado

    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        cont = 0

        for usuario in usuarios:

            cont += 1

            if nome == 'adm' and senha == '0404':

                logado = True

                return redirect('/adm')
            
            if nome == usuario['nome'] and senha == usuario['senha']:
                logado = True
                return redirect('/usuarios')
            
            if cont >= len(usuarios):
                flash('ERRO: LOGIN OU SENHA INVÁLIDOS')
                

        return redirect('/')
    
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('usuarios.json', 'r') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        
        for usuario in usuarios:
            if nome == usuario['nome']:
                flash('ERRO: USUÁRIO JÁ CADASTRADO')
                return redirect('/adm')

        novo_usuario = {
            "nome": nome,
            "senha": senha
        }

        usuarios.append(novo_usuario)

        with open('usuarios.json', 'w') as gravarTemp:
            json.dump(usuarios, gravarTemp, indent=4)

            flash('USUÁRIO CADASTRADO')
            

        return redirect('/adm')
    
@app.route('/excluirUsuario', methods = ['POST'])
def excluirUsuario():
    global logado
    logado = True

    usuario = request.form.get('usuarioExclusao')
    usuarioDict = ast.literal_eval(usuario)

    nome = usuarioDict['nome']

    with open('usuarios.json') as usuariosTemp:
        usuarios= json.load(usuariosTemp)

    for usuario in usuarios:
        if usuario == usuarioDict:
            usuarios.remove(usuario)

            with open('usuarios.json', 'w') as gravarTemp:
                json.dump(usuarios, gravarTemp, indent=4)

    flash(F'{nome} EXCLUIDO COM SUCESSO')

    return redirect('/adm')

@app.route('/upload', methods = ['POST'])
def upload():
    global logado
    logado = True

    arquivo = request.files.get('documento')

    if arquivo is None or arquivo.filename == '':

        flash('ERRO: Nenhum arquivo escolhido')
        return redirect('/usuarios')

    nome_arquivo = arquivo.filename.replace(" ", "-")

    arquivo.save(os.path.join('arquivos', nome_arquivo))

    flash('UPLOAD COM SUCESSO')

    return render_template("usuario.html",)

@app.route('/usuarios')
def usuarios():

    if logado == True:

        arquivos = []

        for documento in os.listdir('arquivos'):
            arquivos.append(documento)

        return render_template("usuario.html", arquivos = arquivos)
    
    return redirect ('/')

@app.route('/download', methods=['POST'])
def download():
    nomeArquivo = request.form.get('arquivosParaDownload')

    return send_from_directory('arquivos', nomeArquivo, as_attachment=True)

if __name__ in "__main__":
    app.run(debug=True)