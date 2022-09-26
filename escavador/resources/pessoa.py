from escavador.resources.helpers.endpoint import Endpoint
from typing import Optional


class Pessoa(Endpoint):

    def por_id(self, id_pessoa: int) -> dict:
        """
        Retorna dados relacionados a uma pessoa pelo seu identificador.
        :param id_pessoa: o ID da pessoa
        :return: dict
        """
        return self.methods.get(f"pessoas/{id_pessoa}")

    def processos(self, id_pessoa: int, *, limit: Optional[int] = None,
                             page: Optional[int] = None) -> dict:
        """
        Retorna os processos de uma pessoa baseado no ID da pessoa.
        :param id_pessoa: o ID da pessoa
        :param page: número da página
        :param limit: limita a quantidade de registros retornados
        :return: dict
        """
        data = {
            'limit': limit,
            'page': page
        }

        return self.methods.get(f"pessoas/{id_pessoa}/processos", data=data)
