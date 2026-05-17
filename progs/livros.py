from progs.database import conexao, cursor

def menu_livros():
    while True:
        print("\n")
        print("="*30)
        print("GESTÃO DE LIVROS")
        print("="*30)
        print("1 - Adicionar Livro")
        print("2 - Listar Livros")
        print("3 - Remover Livro")
        print("0 - Voltar")
        print("="*30)

        op = input("Escolha: ")

        if op == "1":
            adicionar_livro()
        elif op == "2":
            listar_livros()
        elif op == "3":
            remover_livro()
        elif op == "0":
            break
        else:
            print("Opção inválida!")


def adicionar_livro():
    print("\n=== Adicionar Novo Livro ===")

    titulo    = input("Título: ")
    autor     = input("Autor: ")
    editora   = input("Editora: ")
    ano       = input("Ano de Publicação: ")
    categoria = input("Categoria: ")
    quantidade = input("Quantidade: ")

    sql = "INSERT INTO livro (titulo, autor, editora, ano_publicacao, categoria, quantidade) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (titulo, autor, editora, ano, categoria, quantidade)

    cursor.execute(sql, valores)
    conexao.commit()
    print("Livro adicionado com sucesso!")


def listar_livros():
    print("\n=== Lista de Livros ===")

    cursor.execute("SELECT * FROM livro")
    livros = cursor.fetchall()

    if not livros:
        print("Nenhum livro registado.")
        return

    for livro in livros:
        print(f"\nID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | Editora: {livro[3]} | Ano: {livro[4]} | Categoria: {livro[5]} | Quantidade: {livro[6]}")


def remover_livro():
    print("\n=== Remover Livro ===")

    listar_livros()
    id_livro = input("\nID do livro a remover: ")

    cursor.execute("DELETE FROM livro WHERE id_livro = %s", (id_livro,))
    conexao.commit()
    print("Livro removido com sucesso!")