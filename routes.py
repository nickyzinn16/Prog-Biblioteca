from flask import render_template, request, redirect, url_for, session
from progs.database import connection

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
            titulo     = request.form["titulo"]
            autor      = request.form["autor"]
            editora    = request.form["editora"]
            ano        = request.form["ano"]
            categoria  = request.form["categoria"]
            quantidade = request.form["quantidade"]
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO livro (titulo, autor, editora, ano_publicacao, categoria, quantidade) VALUES (%s, %s, %s, %s, %s, %s)",
                        (titulo, autor, editora, ano, categoria, quantidade))
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
        cur.execute("DELETE FROM livro WHERE id_livro = %s", (id,))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for("func_livros"))

    @app.route("/catalogo/<categoria>")
    def catalogo(categoria):
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM livro WHERE categoria = %s", (categoria,))
        livros = cur.fetchall()
        cur.close()
        con.close()
        return render_template(f"catalogos/{categoria}.html", livros=livros)

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
        return render_template("carrinho.html")

    @app.route("/promocoes")
    def promocoes():
        con = connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM livro WHERE promocao = 1")
        livros = cur.fetchall()
        cur.close()
        con.close()
        return render_template("promocoes.html", livros=livros)

    @app.route("/contactos")
    def contactos():
        return render_template("contactos.html")

    @app.route("/perguntas")
    def perguntas():
        return render_template("perguntas.html")

    @app.route("/politicas")
    def politicas():
        return render_template("politicas.html")

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
            nome      = request.form["nome"]
            descricao = request.form["descricao"]
            imagem    = request.form["imagem"]
            con = connection()
            cur = con.cursor()
            cur.execute("INSERT INTO catalogo (nome, descricao, imagem) VALUES (%s, %s, %s)",
                        (nome, descricao, imagem))
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
            preco    = request.form["preco"]
            desconto = request.form["desconto"]
            con = connection()
            cur = con.cursor()
            cur.execute("UPDATE livro SET promocao = 1, preco = %s, desconto = %s WHERE id_livro = %s",
                        (preco, desconto, id_livro))
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