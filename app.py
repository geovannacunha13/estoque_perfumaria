from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from conexao import psycopg2, conn
import re
import os
from werkzeug.utils import secure_filename
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def add_pagamento(tipo_pagamento):
    cur_pagamento = conn.cursor()
    cur_pagamento.execute("INSERT INTO Pagamento (tipo_pagamento) VALUES (%s)", (tipo_pagamento,))
    conn.commit()

def add_perfume(nome_perfume, quantidade, preco, imagem):
    filename = secure_filename(imagem.filename)
    imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    imagem.save(imagem_path)

    cur_perfume = conn.cursor()
    cur_perfume.execute("INSERT INTO Perfume (nome_perfume, quantidade, preco, imagem) VALUES (%s, %s, %s, %s)",
                        (nome_perfume, quantidade, preco, imagem_path))
    conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM perfume"
    cur.execute(s)
    lista_produtos = cur.fetchall()

    for produto in lista_produtos:
        produto_id = produto['idperfumaria']
        imagem_path = produto['imagem']
        produto['imagem'] = imagem_path

    return render_template('index.html', active_page='index', lista_produtos=lista_produtos)

def get_image_path(imagem_path):
    imagem_path = imagem_path.replace('\\', '/')
    return imagem_path

@app.route('/produto', methods=['GET'])
def produto():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM perfume"
    cur.execute(s)
    lista_produtos = cur.fetchall()

    for produto in lista_produtos:
        produto_id = produto['idperfumaria']
        imagem_path = produto['imagem']
        produto['imagem'] = imagem_path

    return render_template('product.html', active_page='produto', lista_produtos=lista_produtos)

def add_cliente(nome, senha, email, cpf, celular):
    cur_cliente = conn.cursor()
    cur_cliente.execute("INSERT INTO cliente (nome, senha, email, cpf, celular) VALUES (%s, %s, %s, %s, %s)",
                        (nome, senha, email, cpf, celular))
    conn.commit()

@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
    cursor = conn.cursor()
    login_alert = None
    register_alert = None
    
    active_tab = request.form.get('tab', 'login')

    if request.method == 'POST':
        if active_tab == 'login':
            email = request.form['email']
            senha = request.form['senha']

            cursor.execute('SELECT * FROM cliente WHERE email = %s AND senha = %s', (email, senha))
            account = cursor.fetchone()

            if account:
                session['loggedin'] = True
                session['id'] = account[0]
                session['nome'] = account[3]
                return redirect(url_for('produto'))
            else:
                login_alert = {'type': 'danger', 'message': 'Usuário ou senha incorretos.'}
        elif active_tab == 'registro':
            nome = request.form['nome']
            senha = request.form['senha']
            email = request.form['email']
            cpf = request.form['cpf']
            celular = request.form['celular']

            cursor.execute('SELECT * FROM cliente WHERE nome = %s', (nome,))
            existing_account = cursor.fetchone()

            if existing_account:
                register_alert = {'type': 'danger', 'message': 'Usuário já existe!'}
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                register_alert = {'type': 'danger', 'message': 'Endereço de e-mail inválido!'}
            elif not re.match(r'[0-9]{11}', cpf):
                register_alert = {'type': 'danger', 'message': 'CPF inválido!'}
            elif not re.match(r'[0-9]+', celular):
                register_alert = {'type': 'danger', 'message': 'Número de celular inválido!'}
            else:
                add_cliente(nome, senha, email, cpf, celular)
                register_alert = {'type': 'success', 'message': 'Registro bem-sucedido!'}

    return render_template('cliente.html', active_tab=active_tab, login_alert=login_alert, register_alert=register_alert)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nome', None)
    return redirect(url_for('cliente'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    alert_message_perfume = None
    alert_type_perfume = None
    alert_message_pagamento = None
    alert_type_pagamento = None

    if request.method == 'POST':
        tipo_pagamento = request.form.get('tipo_pagamento')
        nome_perfume = request.form.get('nome_perfume')
        quantidade = request.form.get('quantidade')
        preco = request.form.get('preco')

        if tipo_pagamento:
            add_pagamento(tipo_pagamento)
            alert_message_pagamento = 'Forma de pagamento cadastrada com sucesso!'
            alert_type_pagamento = 'success'

        elif nome_perfume and quantidade and preco:
            imagem_perfume = request.files.get('imagem_perfume')

            if imagem_perfume and allowed_file(imagem_perfume.filename):
                add_perfume(nome_perfume, quantidade, preco, imagem_perfume)
                alert_message_perfume = 'Perfume cadastrado com sucesso!'
                alert_type_perfume = 'success'

            else:
                alert_message_perfume = 'Por favor, envie uma imagem válida.'
                alert_type_perfume = 'danger'

    cur_pagamento = conn.cursor()
    cur_pagamento.execute("SELECT * FROM Pagamento")
    lista_de_pagamentos = cur_pagamento.fetchall()

    cur_perfume = conn.cursor()
    cur_perfume.execute("SELECT * FROM Perfume")
    lista_de_perfumes = cur_perfume.fetchall()
    
    cur_cliente = conn.cursor()
    cur_cliente.execute("SELECT * FROM cliente")
    lista_cliente = cur_cliente.fetchall()

    return render_template('admin.html',
                           alert_message_perfume=alert_message_perfume,
                           alert_type_perfume=alert_type_perfume,
                           alert_message_pagamento=alert_message_pagamento,
                           alert_type_pagamento=alert_type_pagamento,
                           pagamentos=lista_de_pagamentos,
                           perfumes=lista_de_perfumes,
                           clientes=lista_cliente)

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_pagamento(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM pagamento WHERE idpagamento = {0}'.format(id))
    conn.commit()
    session['deletion_success'] = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'redirect': url_for('admin', active_tab='pagamento')})
    else:
        return redirect(url_for('admin', active_tab='pagamento'))

produtos_no_carrinho = []

@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    total = 0
    cur_pagamento = conn.cursor()
    cur_pagamento.execute("SELECT tipo_pagamento FROM Pagamento")
    opcoes_pagamento = [row[0] for row in cur_pagamento.fetchall()]

    if request.method == 'POST':
        produto_selecionado_id = int(request.form.get('idperfumaria'))
        produto_nome = request.form.get('nome_perfume')
        produto_preco = float(request.form.get('preco'))
        quantidade = 1
        preco_total = quantidade * produto_preco

        produto_selecionado = {
            'idperfumaria': produto_selecionado_id,
            'nome': produto_nome,
            'preco': produto_preco,
            'quantidade': quantidade,
            'preco_total': preco_total
        }

        produtos_no_carrinho.append(produto_selecionado)

    total = sum(produto['preco_total'] for produto in produtos_no_carrinho)

    return render_template('carrinho.html', produtos_carrinho=produtos_no_carrinho, total=total, opcoes_pagamento=opcoes_pagamento)

@app.route('/atualizar-quantidade', methods=['POST'])
def atualizar_quantidade():
    produto_id = int(request.form.get('produto_id'))
    quantidade = int(request.form.get('quantidade'))

    for produto in produtos_no_carrinho:
        if produto['idperfumaria'] == produto_id:
            produto['quantidade'] = quantidade
            produto['preco_total'] = quantidade * produto['preco']

    return redirect(url_for('carrinho'))

@app.route('/remover-do-carrinho', methods=['POST'])
def remover_do_carrinho():
    produto_id = request.form.get('produto_id')

    produtos_no_carrinho[:] = [produto for produto in produtos_no_carrinho if produto['idperfumaria'] != int(produto_id)]

    total = sum(produto['preco_total'] for produto in produtos_no_carrinho)

    return render_template('carrinho.html', produtos_carrinho=produtos_no_carrinho, total=total)

@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    endereco = request.form.get('endereco')
    idcliente = session.get('id')
    idpagamento = request.form.get('forma_pagamento')
    motoboy = "Paulo"
    preco_total = sum(produto['preco_total'] for produto in produtos_no_carrinho)

    cur_pedido = conn.cursor()
    cur_pedido.execute(
        "INSERT INTO Pedido (motoboy, endereco, idcliente, idpagamento, preco_total) VALUES (%s, %s, %s, %s, %s)",
        (motoboy, endereco, idcliente, idpagamento, preco_total)
    )
    conn.commit()

    cur_pedido.execute("SELECT currval('pedido_idpedido_seq')")
    idpedido = cur_pedido.fetchone()[0]

    for produto in produtos_no_carrinho:
        idproduto = produto['idperfumaria']
        quantidade = produto['quantidade']
        preco_produto = produto['preco']
        preco_total_produto = produto['preco_total']

        cur_pedido.execute(
            "INSERT INTO PedidoProduto (idperfumaria, quantidade, preco_unitario, preco_total) VALUES (%s, %s, %s, %s, %s)",
            (idpedido, idproduto, quantidade, preco_produto, preco_total_produto)
        )
        conn.commit()

    produtos_no_carrinho.clear()

    return redirect(url_for('pagina_de_confirmacao'))

if __name__ == "__main__":
    app.run(debug=True)