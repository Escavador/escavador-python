from escavador.resources.helpers.endpoint import Endpoint


class Saldo(Endpoint):

    def quantidade(self) -> dict:
        """
        Retorna a quantidade de créditos do usuário
        :return: dict
        """
        return self.methods.get("quantidade-creditos")
