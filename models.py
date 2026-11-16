from datetime import datetime


class Cliente:
    def __init__(self, nome: str, cpf: str, telefone: str):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone
        }

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(dados["nome"], dados["cpf"], dados["telefone"])

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf} | Tel: {self.telefone})"


class Quarto:
    """Classe base para acomodações do hotel."""
    def __init__(self, numero: int, preco_base: float):
        self.numero = numero
        self.preco_base = preco_base
        self.tipo = "Padrão"

    def calcular_diaria(self) -> float:
        """Método polimórfico: cada subclasse pode aplicar suas próprias taxas."""
        return self.preco_base

    def descrever(self) -> str:
        """Método polimórfico para exibição detalhada."""
        return f"Quarto {self.numero} [{self.tipo}] - Diária: R$ {self.calcular_diaria():.2f}"

    def to_dict(self) -> dict:
        return {
            "numero": self.numero,
            "preco_base": self.preco_base,
            "tipo": self.tipo
        }

    @classmethod
    def from_dict(cls, dados: dict):
        tipo = dados.get("tipo")
        if tipo == "Solteiro":
            return QuartoSolteiro(dados["numero"], dados["preco_base"])
        elif tipo == "Casal":
            return QuartoCasal(dados["numero"], dados["preco_base"])
        elif tipo == "Suíte":
            return Suite(dados["numero"], dados["preco_base"])
        return cls(dados["numero"], dados["preco_base"])


class QuartoSolteiro(Quarto):
    def __init__(self, numero: int, preco_base: float):
        super().__init__(numero, preco_base)
        self.tipo = "Solteiro"

    def calcular_diaria(self) -> float:
        # Sem taxa adicional
        return self.preco_base


class QuartoCasal(Quarto):
    def __init__(self, numero: int, preco_base: float):
        super().__init__(numero, preco_base)
        self.tipo = "Casal"

    def calcular_diaria(self) -> float:
        # Acréscimo de 10% referente à taxa de limpeza dupla
        return self.preco_base * 1.10


class Suite(Quarto):
    def __init__(self, numero: int, preco_base: float):
        super().__init__(numero, preco_base)
        self.tipo = "Suíte"

    def calcular_diaria(self) -> float:
        # Acréscimo de 25% referente a serviços VIP e café no quarto
        return self.preco_base * 1.25

    def descrever(self) -> str:
        base = super().descrever()
        return f"{base} (Inclui Hidromassagem e Serviço VIP)"


class Reserva:
    def __init__(self, id_reserva: int, cpf_cliente: str, numero_quarto: int,
                 check_in: str, check_out: str, valor_total: float, ativa: bool = True):
        self.id_reserva = id_reserva
        self.cpf_cliente = cpf_cliente
        self.numero_quarto = numero_quarto
        self.check_in = check_in    # Formato YYYY-MM-DD
        self.check_out = check_out  # Formato YYYY-MM-DD
        self.valor_total = valor_total
        self.ativa = ativa

    def to_dict(self) -> dict:
        return {
            "id_reserva": self.id_reserva,
            "cpf_cliente": self.cpf_cliente,
            "numero_quarto": self.numero_quarto,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "valor_total": self.valor_total,
            "ativa": self.ativa
        }

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            dados["id_reserva"],
            dados["cpf_cliente"],
            dados["numero_quarto"],
            dados["check_in"],
            dados["check_out"],
            dados["valor_total"],
            dados.get("ativa", True)
        )

    def __str__(self):
        status = "ATIVA" if self.ativa else "CANCELADA"
        in_br = datetime.strptime(self.check_in, "%Y-%m-%d").strftime("%d/%m/%Y")
        out_br = datetime.strptime(self.check_out, "%Y-%m-%d").strftime("%d/%m/%Y")
        return (f"Reserva #{self.id_reserva} [{status}] | Quarto: {self.numero_quarto} | "
                f"Cliente CPF: {self.cpf_cliente} | {in_br} até {out_br} | Total: R$ {self.valor_total:.2f}")
