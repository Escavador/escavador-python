from escavador.resources.helpers.endpoint import Endpoint
from typing import Optional, Dict


class Instituicao(Endpoint):

    def por_id(self, id_instituicao: int) -> Dict:
        """
        Retorna uma instituição de acordo com seu ID
        :argument id_instituicao: o ID da instituição
        :return Dict
        """

        return self.methods.get(f"instituicoes/{id_instituicao}")

    def get_processos_instituicao(self, id_instituicao: int, *, limit: Optional[int] = None,
                                  page: Optional[int] = None) -> Dict:
        """
        Retorna os processos de uma instituição
        :param page: número da página
        :param limit: limita a quantidade de registros retornados
        :argument id_instituicao: o ID da instituição
        :return Dict
        """

        data = {
            'limit': limit,
            'page': page
        }
        return self.methods.get(f"instituicoes/{id_instituicao}/processos", data=data)

    def get_pessoas_instituicao(self, id_instituicao: int, *, limit: Optional[int] = None,
                                page: Optional[int] = None) -> Dict:
        """
        Retorna as pessoas de uma instituição
        :param id_instituicao: o ID da instituição
        :param page: número da página
        :param limit: limita a quantidade de registros retornados
        :return Dict
        """

        data = {
            'limit': limit,
            'page': page
        }
        return self.methods.get(f"instituicoes/{id_instituicao}/pessoas", data=data)
