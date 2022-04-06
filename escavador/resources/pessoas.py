from escavador.resources.endpoint import Endpoint
from typing import Optional


class Pessoa(Endpoint):

    def get(self, id_pessoa: int) -> dict:
        """
        Retorna dados relacionados a uma pessoa pelo seu identificador.
        :param id_pessoa: o ID da pessoa
        :return: dict
        """
        return self.methods.get(f"pessoas/{id_pessoa}")

    def get_processos_pessoa(self, id_pessoa: int, *, limit: Optional[int] = None,
                             page: Optional[int] = None) -> dict:
        """
        Return the process of an person based on the person ID \n
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
