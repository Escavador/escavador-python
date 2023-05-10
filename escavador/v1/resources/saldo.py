from escavador.resources.helpers.endpoint import EndpointV1
from typing import Dict


class Saldo(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def quantidade(cls) -> Dict:
        """
        Retorna a quantidade de créditos do usuário
        :return: Dict
        """
        return cls.methods.get("quantidade-creditos")
