from escavador.resources.helpers.endpoint import EndpointV1
from typing import Optional, Dict


class Pessoa(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def por_id(cls, id_pessoa: int) -> Dict:
        """
        Retorna dados relacionados a uma pessoa pelo seu identificador.
        :param id_pessoa: o ID da pessoa
        :return: Dict
        """
        return cls.methods.get(f"pessoas/{id_pessoa}")

    @classmethod
    def processos(cls, id_pessoa: int, *, limit: Optional[int] = None,
                             page: Optional[int] = None) -> Dict:
        """
        Retorna os processos de uma pessoa baseado no ID da pessoa.
        :param id_pessoa: o ID da pessoa
        :param page: número da página
        :param limit: limita a quantidade de registros retornados
        :return: Dict
        """
        data = {
            'limit': limit,
            'page': page
        }

        return cls.methods.get(f"pessoas/{id_pessoa}/processos", data=data)
