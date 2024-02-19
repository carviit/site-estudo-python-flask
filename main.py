from flask import Flask, get_flashed_messages, render_template, redirect, request, flash, send_from_directory,url_for
import json
import ast
import os
import mysql.connector

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

    conect_BD =  mysql.connector.connect(host = 'localhost', database = 'site_teste', user = 'root', password = '0404') 

    if logado == True:

        conect_BD =  mysql.connector.connect(host = 'localhost', database = 'site_teste', user = 'root', password = '0404') 

        if conect_BD.is_connected():

            cursor = conect_BD.cursor()
            cursor.execute("SELECT * FROM USUARIOS")
            usuarios = cursor.fetchall()
        
        return render_template("administrador.html", usuarios = usuarios)
    
    if logado == False:
        return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    
    global logado

    nome = request.form.get('nome')
    senha = request.form.get('senha')

    conect_BD =  mysql.connector.connect(host = 'localhost', database = 'site_teste', user = 'root', password = '0404') 

    cont = 0

    if conect_BD.is_connected():

        cursor = conect_BD.cursor()
        cursor.execute('SELECT * FROM USUARIOS')

        usuariosBD = cursor.fetchall()

        for usuario in usuariosBD:

            usuarioNome = str(usuario[1])
            usuarioSenha = str(usuario[2])

            cont += 1

            if nome == 'adm' and senha == '0404':

                logado = True

                return redirect('/adm')
            
            if nome == usuarioNome and senha == usuarioSenha:
                logado = True
                return redirect('/usuarios')
            
            if cont >= len(usuariosBD):
                flash('ERRO: LOGIN OU SENHA INVÁLIDOS')
                return redirect('/')
            
    else:        
        return redirect('/')
    
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')

 
    conect_BD = mysql.connector.connect(host='localhost', database='site_teste', user='root', password='0404')

    if conect_BD.is_connected():
        cursor = conect_BD.cursor()
        cursor.execute(f"INSERT INTO USUARIOS VALUES (default, '{nome}', '{senha}')")
        conect_BD.commit()
        flash(f'USUÁRIO CADASTRADO')

    logado = True
    return redirect('/adm')
    
@app.route('/excluirUsuario', methods = ['POST'])
def excluirUsuario():
    global logado
    logado = True

    conect_BD =  mysql.connector.connect(host = 'localhost', database = 'site_teste', user = 'root', password = '0404')
    idUsuarioExclusao = int(request.form.get('usuarioExclusao'))
    nomeUsuario = str(request.form.get('nome'))
    nomeUsuario = nomeUsuario.upper()

    if conect_BD.is_connected():
        cursor = conect_BD.cursor()
        cursor.execute(f"DELETE FROM USUARIOS WHERE id = {idUsuarioExclusao};")
        conect_BD.commit()

    flash(F'{nomeUsuario} EXCLUIDO COM SUCESSO')

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