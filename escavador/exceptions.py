from typing import Dict, Optional


class ApiKeyNotFoundException(KeyError):
    pass


class FailedRequest(Exception):
    """Exceção lançada quando a API retorna um erro.

    Pode ser comparada com uma string representando seu código de erro, ou com um inteiro representando seu
    código de status da resposta.

    :attr status_code: código de status da resposta
    :attr mensagem: mensagem de erro
    :attr erros: detalhamento dos erros encontrados
    """
    status: int
    code: str
    message: str
    errors: Dict

    def __init__(self, status: int,
                 code: str = "",
                 message: str = "",
                 errors: Dict = {},
                 error: str = "",
                 **kwargs):
        self.status = status
        self.code = code
        self.message = message or error  # unauthenticated e "créditos insuficientes" tem estrutura diferente
        self.errors = errors
        if self.status == 401:
            raise self

    def __str__(self):
        return f"Erro {self.code} ({self.status}): {self.message}"

    def __repr__(self):
        return f"{self.__str__()}\n{self.errors}"

    def __eq__(self, other):
        if isinstance(other, int):
            return self.status == other
        elif isinstance(other, str):
            return self.code.upper() == other.upper()
        else:
            return isinstance(other, FailedRequest) and self.code == other.code
