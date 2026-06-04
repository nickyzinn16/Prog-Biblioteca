from flask import render_template, request, redirect, url_for, session
from progs.database import connection
from datetime import date
import os
import time

def init_routes(app):

    @app.route("/")
    def index():
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM catalogo")
        catalogos = cur.fetchall()
        cur.close()
        con.close()
        return render_template("index.html", catalogos=catalogos)

    @app.route("/catalogo/<categoria>")
    def catalogo(categoria):
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM livro WHERE categoria = %s", (categoria,))
        livros = cur.fetchall()
        cur.execute("SELECT imagem FROM catalogo WHERE nome = %s", (categoria,))
        cat = cur.fetchone()
        imagem_catalogo = cat[0] if cat else ''
        cur.close()
        con.close()
        return render_template(f"catalogos/{categoria}.html", livros=livros, imagem_catalogo=imagem_catalogo, nome_catalogo=categoria.capitalize())

    @app.route("/promocoes")
    def promocoes():
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM livro WHERE promocao = 1")
        livros = cur.fetchall()
        cur.close()
        con.close()
        return render_template("promocoes.html", livros=livros)

    @app.route("/perguntas")
    def perguntas():
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM perguntas")
        perguntas = cur.fetchall()
        cur.close()
        con.close()
        return render_template("perguntas.html", perguntas=perguntas)

    @app.route("/contactos")
    def contactos():
        return render_template("contactos.html")

    @app.route("/politicas")
    def politicas():
        return render_template("politicas.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        erro = None
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            con = connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM utilizador WHERE email = %s AND password = %s", (email, password))
            utilizador = cur.fetchone()
            cur.close()
            con.close()
            if utilizador:
                session["id"] = utilizador[0]
                session["nome"] = utilizador[1]
                session["email"] = utilizador[3]
                return redirect(url_for("dashboard_funcionario"))
            else:
                erro = "Email ou password incorretos!"
        return render_template("login.html", erro=erro)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    @app.route("/favoritos")
    def favoritos():
        ids = session.get("favoritos", [])
        livros = []
        if ids:
            con = connection()
            cur = con.cursor()
            formato = ','.join(['%s'] * len(ids))
            cur.execute(f"SELECT * FROM livro WHERE id_livro IN ({formato})", ids)
            livros = cur.fetchall()
            cur.close()
            con.close()
        return render_template("favoritos.html", livros=livros)

    @app.route("/favoritos/adicionar/<int:id_livro>")
    def adicionar_favorito(id_livro):
        if "favoritos" not in session:
            session["favoritos"] = []
        favoritos = session["favoritos"]
        if id_livro not in favoritos:
            favoritos.append(id_livro)
            session["favoritos"] = favoritos
        return redirect(request.referrer)

    @app.route("/favoritos/remover/<int:id_livro>")
    def remover_favorito(id_livro):
        if "favoritos" in session:
            favoritos = session["favoritos"]
            if id_livro in favoritos:
                favoritos.remove(id_livro)
                session["favoritos"] = favoritos
        return redirect(url_for("favoritos"))

    @app.route("/carrinho")
    def carrinho():
        ids = session.get("carrinho", [])
        livros = []
        if ids:
            con = connection()
            cur = con.cursor()
            formato = ','.join(['%s'] * len(ids))
            cur.execute(f"SELECT * FROM livro WHERE id_livro IN ({formato})", ids)
            livros = cur.fetchall()
            cur.close()
            con.close()
        return render_template("carrinho.html", livros=livros)

    @app.route("/carrinho/adicionar/<int:id_livro>")
    def adicionar_carrinho(id_livro):
        if "carrinho" not in session:
            session["carrinho"] = []
        carrinho = session["carrinho"]
        if id_livro not in carrinho:
            carrinho.append(id_livro)
            session["carrinho"] = carrinho
        return redirect(request.referrer)

    @app.route("/carrinho/remover/<int:id_livro>")
    def remover_carrinho(id_livro):
        if "carrinho" in session:
            carrinho = session["carrinho"]
            if id_livro in carrinho:
                carrinho.remove(id_livro)
                session["carrinho"] = carrinho
        return redirect(url_for("carrinho"))

    @app.route("/emprestar/<int:id_livro>", methods=["GET", "POST"])
    def emprestar(id_livro):
        if request.method == "POST":
            nome = request.form["nome"]
            email = request.form["email"]
            telefone = request.form["telefone"]
            data_devolucao = request.form["data_devolucao"]
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO emprestimos_pedidos (id_livro, nome_cliente, email_cliente, telefone_cliente, data_pedido, data_devolucao) VALUES (%s, %s, %s, %s, CURDATE(), %s)",
                        (id_livro, nome, email, telefone, data_devolucao))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("carrinho"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT titulo FROM livro WHERE id_livro = %s", (id_livro,))
        livro = cur.fetchone()
        cur.close()
        con.close()
        return render_template("emprestar.html", livro=livro, id_livro=id_livro)

    @app.route("/comprar/<int:id_livro>", methods=["GET", "POST"])
    def comprar(id_livro):
        if request.method == "POST":
            nome = request.form["nome"]
            email = request.form["email"]
            telefone = request.form["telefone"]
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO compras (id_livro, nome_cliente, email_cliente, telefone_cliente, data_compra) VALUES (%s, %s, %s, %s, CURDATE())", (id_livro, nome, email, telefone))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("carrinho"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT titulo, preco, promocao, desconto FROM livro WHERE id_livro = %s", (id_livro,))
        livro = cur.fetchone()
        cur.close()
        con.close()
        return render_template("comprar.html", livro=livro, id_livro=id_livro)

    @app.route("/funcionario")
    def dashboard_funcionario():
        if not session.get("id"):
            return redirect(url_for("login"))
        return render_template("funcionario/dashboard.html")

    @app.route("/funcionario/livros")
    def func_livros():
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM livro")
        livros = cur.fetchall()
        cur.close()
        con.close()
        return render_template("funcionario/livros.html", livros=livros)

    @app.route("/funcionario/livros/adicionar", methods=["GET", "POST"])
    def func_adicionar_livro():
        if not session.get("id"):
            return redirect(url_for("login"))
        if request.method == "POST":
            titulo = request.form["titulo"]
            autor = request.form["autor"]
            editora = request.form["editora"]
            ano = request.form["ano"]
            categoria = request.form["categoria"]
            quantidade = request.form["quantidade"]
            preco = request.form["preco"]
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO livro (titulo, autor, editora, ano_publicacao, categoria, quantidade, preco) VALUES (%s, %s, %s, %s, %s, %s, %s)", (titulo, autor, editora, ano, categoria, quantidade, preco))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("func_livros"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT nome FROM catalogo")
        catalogos = cur.fetchall()
        cur.close()
        con.close()
        return render_template("funcionario/adicionar_livro.html", catalogos=catalogos)

    @app.route("/funcionario/livros/remover/<int:id>")
    def func_remover_livro(id):
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("DELETE FROM emprestimos_pedidos WHERE id_livro = %s", (id,))
        cur.execute("DELETE FROM compras WHERE id_livro = %s", (id,))
        cur.execute("DELETE FROM livro WHERE id_livro = %s", (id,))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for("func_livros"))

    @app.route("/funcionario/catalogos")
    def func_catalogos():
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM catalogo")
        catalogos = cur.fetchall()
        cur.close()
        con.close()
        return render_template("funcionario/catalogos.html", catalogos=catalogos)

    @app.route("/funcionario/catalogos/adicionar", methods=["GET", "POST"])
    def func_adicionar_catalogo():
        if not session.get("id"):
            return redirect(url_for("login"))
        if request.method == "POST":
            nome = request.form["nome"]
            descricao = request.form["descricao"]
            ficheiro = request.files["imagem"]
            if not ficheiro or ficheiro.filename == '':
                return render_template("funcionario/adicionar_catalogo.html", erro="Nenhum ficheiro selecionado.")
            nome_ficheiro = ficheiro.filename
            extensao = nome_ficheiro.rsplit('.', 1)[-1].lower()
            extensoes_permitidas = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            if extensao not in extensoes_permitidas:
                return render_template("funcionario/adicionar_catalogo.html", erro="Formato não suportado.")
            novo_nome = str(int(time.time())) + '_' + nome_ficheiro
            pasta_imagens = os.path.join(app.root_path, 'static', 'images')
            os.makedirs(pasta_imagens, exist_ok=True)
            ficheiro.save(os.path.join(pasta_imagens, novo_nome))
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO catalogo (nome, descricao, imagem) VALUES (%s, %s, %s)", (nome, descricao, novo_nome))
            con.commit()
            cur.close()
            con.close()
            pasta_templates = os.path.join(app.root_path, 'templates', 'catalogos')
            os.makedirs(pasta_templates, exist_ok=True)
            caminho = os.path.join(pasta_templates, f'{nome}.html')
            if not os.path.exists(caminho):
                html = """<!DOCTYPE html>
<html lang="pt">
    <head>
        <meta charset="utf-8">
        <title>TITULO - Biblioteca</title>
        <link rel="icon" type="image/png" href="{{ url_for('static', filename='images/Logo.png') }}">
        <link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
        <link rel="stylesheet" href="{{ url_for('static', filename='css/footer.css') }}">
        <script src="https://kit.fontawesome.com/35842701b4.js" crossorigin="anonymous"></script>
    </head>
    <body>
        <header class="header">
            <nav class="navbar">
                <div class="logo"><a href="{{ url_for('index') }}"><img src="{{ url_for('static', filename='images/Logo.png') }}" alt="Logo"></a></div>
                <div class="menu">
                    <ul>
                        <li><a href="{{ url_for('index') }}" class="ativo">Início</a></li>
                        <li><a href="{{ url_for('carrinho') }}">Carrinho</a></li>
                        <li><a href="{{ url_for('favoritos') }}">Favoritos</a></li>
                        <li><a href="{{ url_for('promocoes') }}">Promoções</a></li>
                        <li><a href="{{ url_for('login') }}" class="btn-login">Login</a></li>
                    </ul>
                </div>
            </nav>
        </header>
        <div class="conteudo-catalogo">
            <h1 class="titulo-catalogo">{{ nome_catalogo }}</h1>
            <div class="livros-grid">
                {% for livro in livros %}
                <div class="livro">
                    <img src="{{ url_for('static', filename='images/' + imagem_catalogo) }}" alt="{{ livro[1] }}">
                    <div class="info">
                        <h2>{{ livro[1] }}</h2>
                        <p>{{ livro[2] }} | {{ livro[3] }} | {{ livro[4] }}</p>
                        <a href="{{ url_for('adicionar_favorito', id_livro=livro[0]) }}" class="btn-favorito"><i class="fa-solid fa-heart"></i> Adicionar aos Favoritos</a>
                        <a href="{{ url_for('adicionar_carrinho', id_livro=livro[0]) }}" class="btn-carrinho"><i class="fa-solid fa-cart-shopping"></i> Adicionar ao Carrinho</a>
                    </div>
                </div>
                {% else %}
                <p>Nenhum livro disponível nesta categoria.</p>
                {% endfor %}
            </div>
        </div>
        <footer class="footer">
            <div class="footer-container">
                <div class="imagem-footer"><a href="{{ url_for('index') }}"><img src="{{ url_for('static', filename='images/Logo.png') }}" alt="Logo"></a><p>BIBLIOTECA DO MINDELO</p></div>
                <div class="info-uteis">
                    <h4>INFORMAÇÕES ÚTEIS</h4>
                    <ul>
                        <li><a href="{{ url_for('favoritos') }}">Meus Livros Favoritos</a></li>
                        <li><a href="{{ url_for('promocoes') }}">Promoções</a></li>
                        <li><a href="{{ url_for('carrinho') }}">Meu Carrinho</a></li>
                        <li><a href="{{ url_for('perguntas') }}">Perguntas frequentes (FAQ)</a></li>
                    </ul>
                </div>
                <div class="endereco-contactos">
                    <h4>ENDEREÇO & CONTACTOS</h4>
                    <p><a href="https://www.google.com/maps/place/Biblioteca+Municipal+do+Mindelo/@16.8866176,-24.9914655,17z" target="_blank">Biblioteca Municipal do Mindelo</a></p>
                    <p><a href="tel:9959295">+9959295</a></p>
                    <p><a href="mailto:biblioteca@gmail.com">biblioteca@gmail.com</a></p>
                </div>
                <div class="redes-container">
                    <h4>SIGA A BIBLIOTECA NAS REDES SOCIAIS</h4>
                    <div class="redes-sociais">
                        <a href="https://www.facebook.com" target="_blank"><i class="fa-brands fa-facebook"></i></a>
                        <a href="https://www.instagram.com" target="_blank"><i class="fa-brands fa-square-instagram"></i></a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 BIBLIOTECA DO MINDELO - Todos os direitos reservados</p>
                <a href="{{ url_for('politicas') }}">Políticas e Privacidade</a>
            </div>
        </footer>
        <button id="btn-topo">↑</button>
        <script src="{{ url_for('static', filename='javascript/botao.js') }}"></script>
    </body>
</html>"""
                html = html.replace('TITULO', nome.capitalize())
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(html)
            return redirect(url_for("func_catalogos"))
        return render_template("funcionario/adicionar_catalogo.html", erro=None)

    @app.route("/funcionario/catalogos/remover/<int:id>")
    def func_remover_catalogo(id):
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("DELETE FROM catalogo WHERE id_catalogo = %s", (id,))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for("func_catalogos"))

    @app.route("/funcionario/promocoes")
    def func_promocoes():
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM livro WHERE promocao = 1")
        promocoes = cur.fetchall()
        cur.close()
        con.close()
        return render_template("funcionario/promocoes.html", promocoes=promocoes)

    @app.route("/funcionario/promocoes/adicionar", methods=["GET", "POST"])
    def func_adicionar_promocao():
        if not session.get("id"):
            return redirect(url_for("login"))
        if request.method == "POST":
            id_livro = request.form["id_livro"]
            preco = request.form["preco"]
            desconto = request.form["desconto"]
            con = connection()
            cur = con.cursor()
            cur.execute("UPDATE livro SET promocao = 1, preco = %s, desconto = %s WHERE id_livro = %s", (preco, desconto, id_livro))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("func_promocoes"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT id_livro, titulo FROM livro WHERE promocao = 0")
        livros = cur.fetchall()
        cur.close()
        con.close()
        return render_template("funcionario/adicionar_promocao.html", livros=livros)

    @app.route("/funcionario/promocoes/remover/<int:id>")
    def func_remover_promocao(id):
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("UPDATE livro SET promocao = 0, preco = 0, desconto = 0 WHERE id_livro = %s", (id,))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for("func_promocoes"))

    @app.route("/funcionario/perguntas")
    def func_perguntas():
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM perguntas")
        perguntas = cur.fetchall()
        cur.close()
        con.close()
        return render_template("funcionario/perguntas.html", perguntas=perguntas)

    @app.route("/funcionario/perguntas/adicionar", methods=["GET", "POST"])
    def func_adicionar_pergunta():
        if not session.get("id"):
            return redirect(url_for("login"))
        if request.method == "POST":
            pergunta = request.form["pergunta"]
            resposta = request.form["resposta"]
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO perguntas (pergunta, resposta) VALUES (%s, %s)", (pergunta, resposta))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("func_perguntas"))
        return render_template("funcionario/adicionar_pergunta.html")

    @app.route("/funcionario/perguntas/remover/<int:id>")
    def func_remover_pergunta(id):
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("DELETE FROM perguntas WHERE id_pergunta = %s", (id,))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for("func_perguntas"))

    @app.route("/funcionario/emprestimos")
    def func_emprestimos():
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT e.id_emprestimo, l.titulo, e.nome_cliente, e.email_cliente, e.telefone_cliente, e.data_pedido, e.data_devolucao FROM emprestimos_pedidos e JOIN livro l ON e.id_livro = l.id_livro")
        emprestimos = cur.fetchall()
        cur.close()
        con.close()
        return render_template("funcionario/emprestimos.html", emprestimos=emprestimos, today=date.today())

    @app.route("/funcionario/compras")
    def func_compras():
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT c.id_compra, l.titulo, c.nome_cliente, c.email_cliente, c.telefone_cliente, c.data_compra FROM compras c JOIN livro l ON c.id_livro = l.id_livro")
        compras = cur.fetchall()
        cur.close()
        con.close()
        return render_template("funcionario/compras.html", compras=compras)

    @app.route("/funcionario/utilizadores")
    def func_utilizadores():
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM utilizador")
        utilizadores = cur.fetchall()
        cur.close()
        con.close()
        if session.get("email") == "superadmin@biblioteca.cv":
            return render_template("superadmin/utilizadores.html", utilizadores=utilizadores)
        return render_template("funcionario/utilizadores.html", utilizadores=utilizadores)

    @app.route("/funcionario/utilizadores/adicionar", methods=["GET", "POST"])
    def func_adicionar_utilizador():
        if not session.get("id"):
            return redirect(url_for("login"))
        if session.get("email") != "superadmin@biblioteca.cv":
            return redirect(url_for("func_utilizadores"))
        if request.method == "POST":
            nome = request.form["nome"]
            idade = request.form["idade"]
            email = request.form["email"]
            password = request.form["password"]
            telefone = request.form["telefone"]
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO utilizador (nome, idade, email, password, data_registo, telefone) VALUES (%s, %s, %s, %s, CURDATE(), %s)", (nome, idade, email, password, telefone))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("func_utilizadores"))
        return render_template("funcionario/adicionar_utilizador.html")

    @app.route("/funcionario/utilizadores/remover/<int:id>")
    def func_remover_utilizador(id):
        if not session.get("id"):
            return redirect(url_for("login"))
        if session.get("email") != "superadmin@biblioteca.cv":
            return redirect(url_for("func_utilizadores"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT email FROM utilizador WHERE id_utilizador = %s", (id,))
        user = cur.fetchone()
        if user and user[0] == "superadmin@biblioteca.cv":
            cur.close()
            con.close()
            return redirect(url_for("func_utilizadores"))
        cur.execute("DELETE FROM utilizador WHERE id_utilizador = %s", (id,))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for("func_utilizadores"))

    @app.route("/funcionario/utilizadores/senha/<int:id>", methods=["GET", "POST"])
    def func_mudar_senha(id):
        if not session.get("id"):
            return redirect(url_for("login"))
        if session.get("email") != "superadmin@biblioteca.cv":
            return redirect(url_for("func_utilizadores"))
        if request.method == "POST":
            nova_senha = request.form["nova_senha"]
            confirmar_senha = request.form["confirmar_senha"]
            if nova_senha == confirmar_senha:
                con = connection()
                cur = con.cursor()
                cur.execute("UPDATE utilizador SET password = %s WHERE id_utilizador = %s", (nova_senha, id))
                con.commit()
                cur.close()
                con.close()
            return redirect(url_for("func_utilizadores"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM utilizador WHERE id_utilizador = %s", (id,))
        utilizador = cur.fetchone()
        cur.close()
        con.close()
        return render_template("superadmin/mudar_senha.html", utilizador=utilizador)

    @app.route("/funcionario/relatorios")
    def func_relatorios():
        if not session.get("id"):
            return redirect(url_for("login"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM livro")
        total_livros = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM catalogo")
        total_catalogos = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM emprestimos_pedidos")
        total_emprestimos = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM emprestimos_pedidos WHERE data_devolucao < CURDATE()")
        total_expirados = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM emprestimos_pedidos WHERE data_devolucao >= CURDATE() OR data_devolucao IS NULL")
        total_ativos = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM compras")
        total_compras = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM livro WHERE promocao = 1")
        total_promocoes = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM perguntas")
        total_perguntas = cur.fetchone()[0]
        cur.close()
        con.close()
        return render_template("funcionario/relatorios.html",
            total_livros=total_livros, total_catalogos=total_catalogos,
            total_emprestimos=total_emprestimos, total_expirados=total_expirados,
            total_ativos=total_ativos, total_compras=total_compras,
            total_promocoes=total_promocoes, total_perguntas=total_perguntas)

    @app.route("/funcionario/livros/editar/<int:id>", methods=["GET", "POST"])
    def func_editar_livro(id):
        if not session.get("id"):
            return redirect(url_for("login"))
        if request.method == "POST":
            titulo = request.form["titulo"]
            autor = request.form["autor"]
            editora = request.form["editora"]
            ano = request.form["ano"]
            categoria = request.form["categoria"]
            quantidade = request.form["quantidade"]
            preco = request.form["preco"]
            con = connection()
            cur = con.cursor()
            cur.execute("UPDATE livro SET titulo=%s, autor=%s, editora=%s, ano_publicacao=%s, categoria=%s, quantidade=%s, preco=%s WHERE id_livro=%s", (titulo, autor, editora, ano, categoria, quantidade, preco, id))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("func_livros"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM livro WHERE id_livro = %s", (id,))
        livro = cur.fetchone()
        cur.execute("SELECT nome FROM catalogo")
        catalogos = cur.fetchall()
        cur.close()
        con.close()
        return render_template("funcionario/editar_livro.html", livro=livro, catalogos=catalogos)

    @app.route("/funcionario/catalogos/editar/<int:id>", methods=["GET", "POST"])
    def func_editar_catalogo(id):
        if not session.get("id"):
            return redirect(url_for("login"))
        if request.method == "POST":
            nome = request.form["nome"]
            descricao = request.form["descricao"]
            con = connection()
            cur = con.cursor()
            cur.execute("UPDATE catalogo SET nome=%s, descricao=%s WHERE id_catalogo=%s", (nome, descricao, id))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("func_catalogos"))
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM catalogo WHERE id_catalogo = %s", (id,))
        catalogo = cur.fetchone()
        cur.close()
        con.close()
        return render_template("funcionario/editar_catalogo.html", catalogo=catalogo)