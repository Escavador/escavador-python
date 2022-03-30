from escavador.endpoint import Endpoint


class Creditos(Endpoint):

    def get_creditos(self):
        """
        Retorna a quantidade de créditos do usuário
        :return: json
        """
        return self.methods.get("/quantidade-creditos")
