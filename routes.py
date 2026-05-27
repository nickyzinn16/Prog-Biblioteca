from flask import render_template, request, redirect, url_for, session
from progs.database import connection

def init_routes(app):

    # ============================================================
    # ============================================================
    # Rotas Publicas
    # ============================================================
    # ============================================================

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
        cur.close()
        con.close()
        return render_template(f"catalogos/{categoria}.html", livros=livros)

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

    # ============================================================
    # ============================================================
    # Sistema de autenticação
    # ============================================================
    # ============================================================

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
                return redirect(url_for("dashboard_funcionario"))
            else:
                erro = "Email ou password incorretos!"
        return render_template("login.html", erro=erro)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    # ============================================================
    # ============================================================
    # Favoritos
    # ============================================================
    # ============================================================

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

    # ============================================================
    # ============================================================
    # Carrinho
    # ============================================================
    # ============================================================

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

    # ============================================================
    # ============================================================
    # Emprestimos e Compras
    # ============================================================
    # ============================================================

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
        cur.execute("SELECT titulo, preco FROM livro WHERE id_livro = %s", (id_livro,))
        livro = cur.fetchone()
        cur.close()
        con.close()
        return render_template("comprar.html", livro=livro, id_livro=id_livro)

    # ============================================================
    # ============================================================
    # PAinel de administração
    # ============================================================
    # ============================================================

    @app.route("/funcionario")
    def dashboard_funcionario():
        if not session.get("id"):
            return redirect(url_for("login"))
        return render_template("funcionario/dashboard.html")

    # ============================================================
    # ============================================================
    # Administração de Livros
    # ============================================================
    # ============================================================

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
            categoria  = request.form["categoria"]
            quantidade = request.form["quantidade"]
            preco = request.form["preco"]
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO livro (titulo, autor, editora, ano_publicacao, categoria, quantidade, preco) VALUES (%s, %s, %s, %s, %s, %s, %s)", (titulo, autor, editora, ano, categoria, quantidade, preco))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("func_livros"))
        return render_template("funcionario/adicionar_livro.html")

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

    # ============================================================
    # ============================================================
    # Administração de Catálogos
    # ============================================================
    # ============================================================

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
            imagem = request.form["imagem"]
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO catalogo (nome, descricao, imagem) VALUES (%s, %s, %s)", (nome, descricao, imagem))
            con.commit()
            cur.close()
            con.close()
            return redirect(url_for("func_catalogos"))
        return render_template("funcionario/adicionar_catalogo.html")

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

    # ============================================================
    # ============================================================
    # Administração de Promoções
    # ============================================================
    # ============================================================

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

    # ============================================================
    # ============================================================
    # Administração de Perguntas Frequentes
    # ============================================================
    # ============================================================

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

    # ============================================================
    # ============================================================
    # Administração de Empréstimos
    # ============================================================
    # ============================================================

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
        return render_template("funcionario/emprestimos.html", emprestimos=emprestimos)

    # ============================================================
    # ============================================================
    # Administração de Compras
    # ============================================================
    # ============================================================

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

    # ============================================================
    # ============================================================
    # Administração dos Relatórios
    # ============================================================
    # ============================================================

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
        cur.execute("SELECT COUNT(*) FROM compras")
        total_compras = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM livro WHERE promocao = 1")
        total_promocoes = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM perguntas")
        total_perguntas = cur.fetchone()[0]
        cur.close()
        con.close()
        return render_template("funcionario/relatorios.html",
            total_livros=total_livros,
            total_catalogos=total_catalogos,
            total_emprestimos=total_emprestimos,
            total_compras=total_compras,
            total_promocoes=total_promocoes,
            total_perguntas=total_perguntas)