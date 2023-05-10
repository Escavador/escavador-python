from escavador.resources.helpers.endpoint import EndpointV1
from typing import Dict


class Tribunal(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def sistemas_disponiveis(cls) -> Dict:
        """
        Retorna todos os sistemas de tribunais disponiveis
        :return: Dict
        """
        return cls.methods.get("tribunal/origens")

    @classmethod
    def detalhes(cls, sigla_tribunal: str) -> Dict:
        """
        Retorna os detalhes do tribunal enviado
        :param sigla_tribunal: A sigla do sistema de tribunal pesquisado
        :return: Dict
        """
        return cls.methods.get(f"tribunal/origens/{sigla_tribunal}")
