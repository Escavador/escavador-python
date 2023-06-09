from escavador.resources.helpers.endpoint import EndpointV1
from typing import Dict


class BuscaAssincrona(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def por_id(cls, id: int) -> Dict:
        """
        Retorna dados de uma busca assíncrona pelo id
        :param id: o ID da busca assíncrona
        :return: Dict
        """
        return cls.methods.get(f"async/resultados/{id}")

    @classmethod
    def resultados(cls) -> Dict:
        """
        Consultar todos os resultados das buscas assíncrona
        :return: Dict
        :return:
        """
        return cls.methods.get("async/resultados")