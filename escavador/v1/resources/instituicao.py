from escavador.resources.helpers.endpoint import EndpointV1
from typing import Optional, Dict


class Instituicao(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def por_id(cls, id_instituicao: int) -> Dict:
        """
        Retorna uma instituição de acordo com seu ID
        :argument id_instituicao: o ID da instituição
        :return Dict
        """

        return cls.methods.get(f"instituicoes/{id_instituicao}")

    @classmethod
    def get_processos_instituicao(cls, id_instituicao: int, *, limit: Optional[int] = None,
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
        return cls.methods.get(f"instituicoes/{id_instituicao}/processos", data=data)

    @classmethod
    def get_pessoas_instituicao(cls, id_instituicao: int, *, limit: Optional[int] = None,
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
        return cls.methods.get(f"instituicoes/{id_instituicao}/pessoas", data=data)
