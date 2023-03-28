from typing import Dict, Optional


class ApiKeyNotFoundException(KeyError):
    pass


class FailedRequest(Exception):
    """Exceção lançada quando a API retorna um erro.

    :attr status_code: código de status da resposta
    :attr mensagem: mensagem de erro
    :attr erros: detalhamento dos erros encontrados
    """
    status: int
    code: str
    message: str
    errors: Dict

    def __init__(self, status: int, code: str = "", message: str = "", errors: Optional[Dict] = None, **kwargs):
        self.status = status
        self.code = code
        self.message = message
        self.errors = errors

    def __str__(self):
        return f"Erro {self.code} ({self.status}): {self.message}"

    def __repr__(self):
        return f"{self.__str__()}\n{self.errors}"

    def __eq__(self, other):
        if isinstance(other, int):
            return self.status == other
        elif isinstance(other, str):
            return self.code == other
        else:
            return isinstance(other, FailedRequest) and self.code == other.code
