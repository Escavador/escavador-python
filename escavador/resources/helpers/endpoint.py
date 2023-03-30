import abc
from typing import Optional, Dict

from escavador.method import Method


class Endpoint(object):

    def __init__(self, api_version: Optional[int] = None):
        if api_version:
            self.methods = Method(api_version)


class DataEndpoint(Endpoint):
    """Um endpoint que não precisa ser instanciado e também representa um objeto retornado pela API

    Exclusivamente usado na API V2.
    """
    __metaclass__ = abc.ABCMeta
    methods = Method(api_version=2)
    last_valid_cursor: Optional[str] = ""  # se não definido pela classe filha, é sempre uma string vazia

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json_dict: Optional[Dict], ultimo_cursor: str) -> Optional["DataEndpoint"]:
        """Constrói um objeto a partir de um dicionário (json)"""
        pass
