import json
import os
from models import Cliente, Quarto, Reserva

ARQUIVO_DADOS = "dados_hotel.json"


def salvar_dados(clientes: list, quartos: list, reservas: list) -> None:
    """Converte os objetos em dicionários e salva no arquivo JSON."""
    estrutura = {
        "clientes": [c.to_dict() for c in clientes],
        "quartos": [q.to_dict() for q in quartos],
        "reservas": [r.to_dict() for r in reservas]
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(estrutura, arquivo, indent=4, ensure_ascii=False)


def carregar_dados() -> tuple:
    """Lê o arquivo JSON e reconstrói as listas de objetos."""
    if not os.path.exists(ARQUIVO_DADOS):
        return [], [], []

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            estrutura = json.load(arquivo)

        clientes = [Cliente.from_dict(c) for c in estrutura.get("clientes", [])]
        quartos = [Quarto.from_dict(q) for q in estrutura.get("quartos", [])]
        reservas = [Reserva.from_dict(r) for r in estrutura.get("reservas", [])]
        return clientes, quartos, reservas
    except (json.JSONDecodeError, KeyError):
        return [], [], []
