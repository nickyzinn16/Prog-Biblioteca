from progs import livros, utilizadores, emprestimos

def menu_principal():
    while True:
        print("\n")
        print("="*30)
        print("SISTEMA DE GESTÃO DE BIBLIOTECA")
        print("="*30)
        print("1 - Gerir Livros")
        print("2 - Gerir Utilizadores")
        print("3 - Gerir Empréstimos")
        print("0 - Sair")
        print("="*30)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            livros.menu_livros()
        elif opcao == "2":
            utilizadores.menu_utilizadores()
        elif opcao == "3":
            emprestimos.menu_emprestimos()
        elif opcao == "0":
            print("Programa terminado.")
            break
        else:
            print("Opção inválida!")