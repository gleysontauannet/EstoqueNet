import funcoes


def ler_int(msg, minimo=0):
    while True:
        try:
            valor = int(input(msg))
            if valor < minimo:
                print(f"Digite um número maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")


def ler_preco(msg):
    while True:
        try:
            valor = float(input(msg).replace(",", "."))
            if valor < 0:
                print("O preço não pode ser negativo.")
                continue
            return valor
        except ValueError:
            print("Preço inválido. Exemplo: 49.90")


def mostrar_produtos(produtos):
    if not produtos:
        print("\nNenhum produto cadastrado.")
        return
    print(f"\n{'ID':<4}{'Nome':<25}{'Preço':>10}{'Estoque':>9}"
          f"{'P':>5}{'M':>5}{'G':>5}{'GG':>5}{'XG':>5}")
    print("-" * 73)
    for p in produtos:
        print(f"{p['id']:<4}{p['nome']:<25}{p['preco']:>10.2f}{p['quantidade_estoque']:>9}"
              f"{p['tam_p']:>5}{p['tam_m']:>5}{p['tam_g']:>5}{p['tam_gg']:>5}{p['tam_xg']:>5}")


def menu_cadastrar():
    print("\n--- Cadastrar produto ---")
    nome = input("Nome: ").strip()
    if not nome:
        print("O nome é obrigatório.")
        return
    preco = ler_preco("Preço: ")
    estoque = ler_int("Quantidade em estoque: ")
    p = ler_int("Qtd tamanho P: ")
    m = ler_int("Qtd tamanho M: ")
    g = ler_int("Qtd tamanho G: ")
    gg = ler_int("Qtd tamanho GG: ")
    xg = ler_int("Qtd tamanho XG: ")
    novo_id = funcoes.cadastrar_produto(nome, preco, estoque, p, m, g, gg, xg)
    print(f"Produto cadastrado com ID {novo_id}.")


def menu_editar():
    print("\n--- Editar produto ---")
    mostrar_produtos(funcoes.listar_produtos())
    id_produto = ler_int("\nID do produto a editar: ", minimo=1)
    produto = funcoes.buscar_produto(id_produto)
    if not produto:
        print("Produto não encontrado.")
        return

    opcoes = {
        "1": ("nome", "Nome"),
        "2": ("preco", "Preço"),
        "3": ("quantidade_estoque", "Quantidade em estoque"),
        "4": ("tam_p", "Tamanho P"),
        "5": ("tam_m", "Tamanho M"),
        "6": ("tam_g", "Tamanho G"),
        "7": ("tam_gg", "Tamanho GG"),
        "8": ("tam_xg", "Tamanho XG"),
    }
    print("\nO que deseja alterar?")
    for k, (_, rotulo) in opcoes.items():
        print(f"{k} - {rotulo}")
    escolha = input("Opção: ").strip()
    if escolha not in opcoes:
        print("Opção inválida.")
        return

    coluna, rotulo = opcoes[escolha]
    if coluna == "nome":
        novo = input("Novo nome: ").strip()
        if not novo:
            print("Nome vazio, nada alterado.")
            return
    elif coluna == "preco":
        novo = ler_preco("Novo preço: ")
    else:
        novo = ler_int(f"Nova quantidade ({rotulo}): ")

    if funcoes.editar_produto(id_produto, **{coluna: novo}):
        print("Produto atualizado.")
    else:
        print("Nada foi alterado.")


def menu_excluir():
    print("\n--- Excluir produto ---")
    mostrar_produtos(funcoes.listar_produtos())
    id_produto = ler_int("\nID do produto a excluir: ", minimo=1)
    produto = funcoes.buscar_produto(id_produto)
    if not produto:
        print("Produto não encontrado.")
        return
    confirma = input(f"Excluir '{produto['nome']}'? (s/n): ").strip().lower()
    if confirma == "s":
        funcoes.excluir_produto(id_produto)
        print("Produto excluído.")
    else:
        print("Operação cancelada.")


def main():
    while True:
        print("\n===== SISTEMA DE ESTOQUE =====")
        print("1 - Cadastrar produto")
        print("2 - Visualizar produtos")
        print("3 - Editar produto")
        print("4 - Excluir produto")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                menu_cadastrar()
            elif opcao == "2":
                mostrar_produtos(funcoes.listar_produtos())
            elif opcao == "3":
                menu_editar()
            elif opcao == "4":
                menu_excluir()
            elif opcao == "0":
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida.")
        except Exception as erro:
            print(f"Erro ao acessar o banco: {erro}")


if __name__ == "__main__":
    main()