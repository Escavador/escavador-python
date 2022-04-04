from escavador.resources.endpoint import Endpoint


class Saldo(Endpoint):

    def get(self):
        """
        Retorna a quantidade de créditos do usuário
        :return: json
        """
        return self.methods.get("quantidade-creditos")
