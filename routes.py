from flask import render_template, request, redirect, url_for, session
from progs.database import connection

def init_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")

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

    @app.route("/carrinho")
    def carrinho():
        return render_template("carrinho.html")

    @app.route("/favoritos")
    def favoritos():
        return render_template("favoritos.html")

    @app.route("/promocoes")
    def promocoes():
        return render_template("promocoes.html")

    @app.route("/contactos")
    def contactos():
        return render_template("contactos.html")

    @app.route("/perguntas")
    def perguntas():
        return render_template("perguntas.html")

    @app.route("/politicas")
    def politicas():
        return render_template("politicas.html")