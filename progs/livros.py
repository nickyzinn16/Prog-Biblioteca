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
            print("Adicionar livro")

        elif op == "2":
            print("Listar livros")

        elif op == "3":
            print("Remover livro")

        elif op == "0":
            break

        else:
            print("Opção inválida!")