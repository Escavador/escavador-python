from escavador.resources.helpers.endpoint import EndpointV1
from typing import Dict

class Movimentacao(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def por_id(cls, id_movimentacao: int) -> Dict:
        """
        Retorna uma movimentação pelo seu identificador
        :param id_movimentacao: o ID da movimentação
        :return: Dict
        """
        return cls.methods.get(f"movimentacoes/{id_movimentacao}")
