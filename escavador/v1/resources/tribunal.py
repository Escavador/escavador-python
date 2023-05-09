from escavador.resources.helpers.endpoint import Endpoint
from typing import Dict


class Tribunal(Endpoint):

    def __init__(self):
        super().__init__(api_version=1)

    def sistemas_disponiveis(self) -> Dict:
        """
        Retorna todos os sistemas de tribunais disponiveis
        :return: Dict
        """
        return self.methods.get("tribunal/origens")

    def detalhes(self, sigla_tribunal: str) -> Dict:
        """
        Retorna os detalhes do tribunal enviado
        :param sigla_tribunal: A sigla do sistema de tribunal pesquisado
        :return: Dict
        """
        return self.methods.get(f"tribunal/origens/{sigla_tribunal}")
