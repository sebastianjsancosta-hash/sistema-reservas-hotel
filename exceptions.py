class ErroHotel(Exception):
    """Exceção base para erros do sistema de reservas do hotel."""
    pass


class QuartoIndisponivelError(ErroHotel):
    """Lançada quando o quarto já possui reserva no período solicitado."""
    pass


class DataInvalidaError(ErroHotel):
    """Lançada quando as datas informadas são inconsistentes (ex: check-out antes do check-in)."""
    pass


class RegistroNaoEncontradoError(ErroHotel):
    """Lançada quando um cliente, quarto ou reserva não é encontrado."""
    pass


class DadosInvalidosError(ErroHotel):
    """Lançada quando um dado digitado é inválido (ex: CPF incompleto, texto no lugar de número)."""
    pass


class ArquivoCorrompidoError(ErroHotel):
    """Lançada quando o arquivo de dados existe, mas não pode ser lido corretamente."""
    pass