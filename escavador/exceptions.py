from typing import List, Dict, Optional


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
        return self.__str__()
