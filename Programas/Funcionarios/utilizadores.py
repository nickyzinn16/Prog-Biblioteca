def menu_utilizadores():
    while True:
        print("\n")
        print("="*30)
        print("GESTÃO DE UTILIZADORES")
        print("="*30)
        print("1 - Adicionar Utilizador")
        print("2 - Listar Utilizadores")
        print("3 - Remover Utilizador")
        print("0 - Voltar")
        print("="*30)

        op = input("Escolha: ")

        if op == "1":
            menu_adicionar_utilizador()

        elif op == "2":
            listar_utilizadores()

        elif op == "3":
            remover_utilizador()

        elif op == "0":
            break

        else:
            print("Opção inválida!")


# ============================================================================= #
# ======================================= Opcao 1 ============================= #
# ============================================================================= #
funcionarios = []
clientes = []

def menu_adicionar_utilizador():
    while True:
        print("\n === Tipo de Utilizador ===")
        print("1 - Adicionar Funcionário")
        print("2 - Adicionar Cliente")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            adicionar_funcionario()
            break

        elif op == "2":
            adicionar_cliente()
            break

        elif op == "0":
            break

        else:
            print("Opção inválida!")


def adicionar_funcionario():
    print("\n === Adicionar Funcionario ===")

    nome = input("Nome Completo: ")
    identificacao = input("Bi: ")
    data_nascimento = input("Data de Nascimento: ")
    email = input("Email: ")
    telefone = input("Telefone: ")
    endereco = input("Endereço: ")

    funcionario = {
        "nome": nome,
        "id": identificacao,
        "data_nascimento": data_nascimento,
        "email": email,
        "telefone": telefone,
        "endereco": endereco
    }

    funcionarios.append(funcionario)
    print("Utilizador adicionado com sucesso.")

# ============================================================================= #
# ============================================================================= #
# ============================================================================= #

