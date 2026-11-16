from datetime import datetime
from models import Cliente, QuartoSolteiro, QuartoCasal, Suite, Reserva
from exceptions import (
    ErroHotel,
    QuartoIndisponivelError,
    DataInvalidaError,
    RegistroNaoEncontradoError
)
from storage import salvar_dados, carregar_dados


def ler_data(mensagem: str) -> datetime:
    """Converte uma string DD/MM/AAAA em objeto datetime."""
    texto = input(mensagem).strip()
    try:
        return datetime.strptime(texto, "%d/%m/%Y")
    except ValueError:
        raise DataInvalidaError("Formato de data inválido. Use DD/MM/AAAA (ex: 20/11/2026).")


def verificar_disponibilidade(numero_quarto: int, inicio: datetime, fim: datetime, reservas: list) -> bool:
    """Verifica se há conflito de datas com reservas ativas para o mesmo quarto."""
    for res in reservas:
        if res.ativa and res.numero_quarto == numero_quarto:
            res_inicio = datetime.strptime(res.check_in, "%Y-%m-%d")
            res_fim = datetime.strptime(res.check_out, "%Y-%m-%d")
            if inicio < res_fim and fim > res_inicio:
                return False
    return True


def cadastrar_cliente(clientes: list) -> None:
    print("\n--- CADASTRO DE CLIENTE ---")
    nome = input("Nome completo: ").strip()
    cpf = input("CPF (apenas números): ").strip()
    telefone = input("Telefone: ").strip()

    if not nome or not cpf:
        raise ValueError("Nome e CPF são obrigatórios.")

    for c in clientes:
        if c.cpf == cpf:
            raise ValueError("Já existe um cliente cadastrado com este CPF.")

    clientes.append(Cliente(nome, cpf, telefone))
    print("Cliente cadastrado com sucesso!")


def remover_cliente(clientes: list, reservas: list) -> None:
    print("\n--- REMOVER CLIENTE ---")
    if not clientes:
        raise RegistroNaoEncontradoError("Nenhum cliente cadastrado.")

    cpf = input("Digite o CPF do cliente que deseja remover: ").strip()
    cliente = next((c for c in clientes if c.cpf == cpf), None)

    if not cliente:
        raise RegistroNaoEncontradoError("Cliente não encontrado.")

    for r in reservas:
        if r.cpf_cliente == cpf and r.ativa:
            raise ErroHotel("Este cliente possui reserva ativa. Cancele a reserva primeiro.")

    clientes.remove(cliente)
    print(f"Cliente {cliente.nome} removido com sucesso!")


def cadastrar_quarto(quartos: list) -> None:
    print("\n--- CADASTRO DE QUARTO ---")
    numero = int(input("Número do quarto: "))
    for q in quartos:
        if q.numero == numero:
            raise ValueError("Já existe um quarto cadastrado com este número.")

    print("Tipos de acomodação: [1] Solteiro | [2] Casal | [3] Suíte")
    opcao_tipo = input("Escolha o tipo: ").strip()
    preco = float(input("Valor base da diária (R$): "))

    if preco <= 0:
        raise ValueError("O valor da diária deve ser maior que zero.")

    if opcao_tipo == "1":
        quarto = QuartoSolteiro(numero, preco)
    elif opcao_tipo == "2":
        quarto = QuartoCasal(numero, preco)
    elif opcao_tipo == "3":
        quarto = Suite(numero, preco)
    else:
        raise ValueError("Tipo de quarto inválido.")

    quartos.append(quarto)
    print(f"Quarto {numero} ({quarto.tipo}) cadastrado com sucesso!")


def realizar_reserva(clientes: list, quartos: list, reservas: list) -> None:
    print("\n--- NOVA RESERVA ---")
    cpf = input("CPF do cliente: ").strip()
    cliente = next((c for c in clientes if c.cpf == cpf), None)
    if not cliente:
        raise RegistroNaoEncontradoError("Cliente não encontrado. Cadastre-o primeiro.")

    if not quartos:
        raise RegistroNaoEncontradoError("Nenhum quarto cadastrado no sistema.")

    print("\nQuartos disponíveis no hotel:")
    for q in quartos:
        print(f"  - {q.descrever()}")

    num_quarto = int(input("\nNúmero do quarto desejado: "))
    quarto = next((q for q in quartos if q.numero == num_quarto), None)
    if not quarto:
        raise RegistroNaoEncontradoError("Quarto não encontrado.")

    data_in = ler_data("Data de Check-in (DD/MM/AAAA): ")
    data_out = ler_data("Data de Check-out (DD/MM/AAAA): ")

    if data_out <= data_in:
        raise DataInvalidaError("A data de check-out deve ser posterior à data de check-in.")

    if not verificar_disponibilidade(num_quarto, data_in, data_out, reservas):
        raise QuartoIndisponivelError(f"O quarto {num_quarto} já está reservado neste período.")

    dias = (data_out - data_in).days
    valor_total = dias * quarto.calcular_diaria()
    novo_id = len(reservas) + 1

    nova_reserva = Reserva(
        id_reserva=novo_id,
        cpf_cliente=cliente.cpf,
        numero_quarto=quarto.numero,
        check_in=data_in.strftime("%Y-%m-%d"),
        check_out=data_out.strftime("%Y-%m-%d"),
        valor_total=valor_total
    )
    reservas.append(nova_reserva)
    print(f"\nReserva #{novo_id} confirmada para {cliente.nome}!")
    print(f"Período: {dias} diária(s) | Valor Total: R$ {valor_total:.2f}")


def listar_reservas(reservas: list) -> None:
    print("\n--- LISTA DE RESERVAS ---")
    if not reservas:
        print("Nenhuma reserva registrada.")
        return
    for r in reservas:
        print(r)


def cancelar_reserva(reservas: list) -> None:
    print("\n--- CANCELAR RESERVA ---")
    id_res = int(input("Informe o ID da reserva: "))
    reserva = next((r for r in reservas if r.id_reserva == id_res), None)

    if not reserva:
        raise RegistroNaoEncontradoError("Reserva não encontrada.")
    if not reserva.ativa:
        raise ErroHotel("Esta reserva já está cancelada.")

    reserva.ativa = False
    print(f"Reserva #{id_res} cancelada com sucesso.")


def menu():
    clientes, quartos, reservas = carregar_dados()

    while True:
        print("\n=========================================")
        print("      SISTEMA DE RESERVAS DE HOTEL       ")
        print("=========================================")
        print("1. Cadastrar Cliente")
        print("2. Cadastrar Quarto")
        print("3. Listar Quartos e Diárias")
        print("4. Realizar Reserva")
        print("5. Listar Reservas")
        print("6. Cancelar Reserva")
        print("7. Remover Cliente")
        print("0. Sair e Salvar")
        print("=========================================")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar_cliente(clientes)
                salvar_dados(clientes, quartos, reservas)
            elif opcao == "2":
                cadastrar_quarto(quartos)
                salvar_dados(clientes, quartos, reservas)
            elif opcao == "3":
                print("\n--- QUARTOS CADASTRADOS ---")
                if not quartos:
                    print("Nenhum quarto cadastrado.")
                for q in quartos:
                    print(q.descrever())
            elif opcao == "4":
                realizar_reserva(clientes, quartos, reservas)
                salvar_dados(clientes, quartos, reservas)
            elif opcao == "5":
                listar_reservas(reservas)
            elif opcao == "6":
                cancelar_reserva(reservas)
                salvar_dados(clientes, quartos, reservas)
            elif opcao == "7":
                remover_cliente(clientes, reservas)
                salvar_dados(clientes, quartos, reservas)
            elif opcao == "0":
                salvar_dados(clientes, quartos, reservas)
                print("Dados salvos. Encerrando o sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")

        except ErroHotel as e:
            print(f"\n[AVISO DO SISTEMA]: {e}")
        except ValueError as e:
            print(f"\n[ERRO DE ENTRADA]: {e}")
        except Exception as e:
            print(f"\n[ERRO INESPERADO]: {e}")


if __name__ == "__main__":
    menu()