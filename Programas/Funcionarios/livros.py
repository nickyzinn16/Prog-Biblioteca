lista_livros = []

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
            print("Listar livros")

        elif op == "3":
            print("Remover livro")

        elif op == "0":
            break

        else:
            print("Opção inválida!")


# ============================================================================= #
# ======================================= Opcao 1 ============================= #
# ============================================================================= #
livro = []
def adicionar_livro():
    print("\n=== Adicionar Novo Livro ===")

    autores = input("Autor(es): ")
    titulo = input("Título: ")
    subtitulo = input("Subtítulo: ")
    editora = input("Editora: ")
    ano = input("Ano de Publicação: ")
    edicao = input("Edição: ")
    local = input("Local de Publicação: ")
    paginas = input("Número de Páginas: ")
    categoria = input("Categoria: ")

    livro = {
        "autores": autores,
        "titulo": titulo,
        "subtitulo": subtitulo,
        "editora": editora,
        "ano": ano,
        "edicao": edicao,
        "local": local,
        "paginas": paginas,
        "categoria": categoria
    }

    lista_livros.append(livro)
    print("Livro adicionado com sucesso")

# ============================================================================= #
# ============================================================================= #
# ============================================================================= #