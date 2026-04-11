# Sistema de Gestão de Biblioteca

def menu_principal():
    while True:
        print("\n")
        print("="*40)
        print("SISTEMA DE GESTÃO DE BIBLIOTECA")
        print("="*40)
        print("1 - Gerir Livros")
        print("2 - Gerir Utilizadores")
        print("3 - Gerir Empréstimos")
        print("0 - Sair")
        print("="*40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Entrou em Gestão de Livros")

        elif opcao == "2":
            print("Entrou em Gestão de Utilizadores")

        elif opcao == "3":
            print("Entrou em Gestão de Empréstimos")

        elif opcao == "0":
            print("Programa terminado.")
            break

        else:
            print("Opção inválida! Tenta novamente.")


menu_principal()