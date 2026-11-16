import json
import os
import shutil
from models import Cliente, Quarto, Reserva
from exceptions import ArquivoCorrompidoError

ARQUIVO_DADOS = "dados_hotel.json"


def salvar_dados(clientes: list, quartos: list, reservas: list) -> None:
    """Converte os objetos em dicionários e salva no arquivo JSON.

    Grava primeiro em um arquivo temporário e depois substitui o original,
    para que uma falha no meio da gravação não corrompa os dados.
    """
    estrutura = {
        "clientes": [c.to_dict() for c in clientes],
        "quartos": [q.to_dict() for q in quartos],
        "reservas": [r.to_dict() for r in reservas]
    }
    temporario = ARQUIVO_DADOS + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(estrutura, arquivo, indent=4, ensure_ascii=False)
    os.replace(temporario, ARQUIVO_DADOS)


def carregar_dados() -> tuple:
    """Lê o arquivo JSON e reconstrói as listas de objetos.

    Se o arquivo não existir, devolve listas vazias (primeira execução).
    Se existir mas estiver corrompido, guarda uma cópia (.bak) e lança
    ArquivoCorrompidoError, em vez de devolver listas vazias em silêncio
    (o que faria o próximo salvamento apagar os dados).
    """
    if not os.path.exists(ARQUIVO_DADOS):
        return [], [], []

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            estrutura = json.load(arquivo)

        clientes = [Cliente.from_dict(c) for c in estrutura.get("clientes", [])]
        quartos = [Quarto.from_dict(q) for q in estrutura.get("quartos", [])]
        reservas = [Reserva.from_dict(r) for r in estrutura.get("reservas", [])]
        return clientes, quartos, reservas
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
        copia = ARQUIVO_DADOS + ".bak"
        shutil.copyfile(ARQUIVO_DADOS, copia)
        raise ArquivoCorrompidoError(
            f"O arquivo '{ARQUIVO_DADOS}' está corrompido ou fora do formato esperado. "
            f"Uma cópia foi guardada em '{copia}'."
        )