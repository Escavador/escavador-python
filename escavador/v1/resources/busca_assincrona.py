from escavador.resources.helpers.endpoint import Endpoint
from typing import Dict


class BuscaAssincrona(Endpoint):

    def __init__(self):
        super().__init__(api_version=1)

    def por_id(self, id: int) -> Dict:
        """
        Retorna dados de uma busca assíncrona pelo id
        :param id: o ID da busca assíncrona
        :return: Dict
        """
        return self.methods.get(f"async/resultados/{id}")

    def resultados(self) -> Dict:
        """
        Consultar todos os resultados das buscas assíncrona
        :return: Dict
        :return:
        """
        return self.methods.get("async/resultados")