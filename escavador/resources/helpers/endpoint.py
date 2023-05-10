import abc
from typing import Optional, Dict

from escavador.method import Method


class Endpoint(object):
    """Um endpoint da API.

    :attr methods: métodos http disponíveis para o endpoint. Deve ser inicializado na classe filha.
    """
    methods: Method = None


class EndpointV1(Endpoint):
    """Um endpoint da API V1 que não precisa ser instanciado.

    :attr methods: métodos http disponíveis para o endpoint
    """
    methods = Method(api_version=1)


class DataEndpoint(Endpoint):
    """Um endpoint que não precisa ser instanciado e também representa um objeto retornado pela API

    Exclusivamente usado na API V2.

    :attr methods: métodos http disponíveis para o endpoint
    :attr last_valid_cursor: cursor retornado pela última requisição válida
    """
    __metaclass__ = abc.ABCMeta
    methods = Method(api_version=2)
    last_valid_cursor: Optional[str] = ""  # se não definido pela classe filha, é sempre uma string vazia

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json_dict: Optional[Dict], ultimo_cursor: str) -> Optional["DataEndpoint"]:
        """Constrói um objeto a partir de um dicionário (json)"""
        pass
