from progs.database import conexao, cursor

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


def menu_adicionar_utilizador():
    while True:
        print("\n === Tipo de Utilizador ===")
        print("1 - Adicionar Funcionário")
        print("2 - Adicionar Cliente")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            adicionar_utilizador("funcionario")
            break
        elif op == "2":
            adicionar_utilizador("cliente")
            break
        elif op == "0":
            break
        else:
            print("Opção inválida!")


def adicionar_utilizador(tipo):
    print(f"\n === Adicionar {tipo.capitalize()} ===")

    nome     = input("Nome Completo: ")
    idade    = input("Idade: ")
    email    = input("Email: ")
    password = input("Password: ")
    telefone = input("Telefone: ")

    sql = "INSERT INTO utilizador (nome, idade, email, password, tipo_utilizador, data_registo, telefone) VALUES (%s, %s, %s, %s, %s, CURDATE(), %s)"
    valores = (nome, idade, email, password, tipo, telefone)

    cursor.execute(sql, valores)
    conexao.commit()
    print(f"{tipo.capitalize()} adicionado com sucesso!")


def listar_utilizadores():
    print("\n=== Lista de Utilizadores ===")

    cursor.execute("SELECT * FROM utilizador")
    utilizadores = cursor.fetchall()

    if not utilizadores:
        print("Nenhum utilizador registado.")
        return

    for u in utilizadores:
        print(f"\nID: {u[0]} | Nome: {u[1]} | Idade: {u[2]} | Email: {u[3]} | Tipo: {u[5]} | Telefone: {u[7]}")


def remover_utilizador():
    print("\n=== Remover Utilizador ===")

    listar_utilizadores()
    id_utilizador = input("\nID do utilizador a remover: ")

    cursor.execute("DELETE FROM utilizador WHERE id_utilizador = %s", (id_utilizador,))
    conexao.commit()
    print("Utilizador removido com sucesso!")