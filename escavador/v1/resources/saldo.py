from escavador.resources.helpers.endpoint import Endpoint
from typing import Dict


class Saldo(Endpoint):

    def __init__(self):
        super().__init__(api_version=1)

    def quantidade(self) -> Dict:
        """
        Retorna a quantidade de créditos do usuário
        :return: Dict
        """
        return self.methods.get("quantidade-creditos")
