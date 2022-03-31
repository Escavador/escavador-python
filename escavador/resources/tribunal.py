from escavador.resources.endpoint import Endpoint


class Tribunal(Endpoint):

    def get_sistemas_tribunais_disponiveis(self):
        """
        Retorna todos os sistemas de tribunais disponiveis
        :return: json contendo todos os sistemas de tribunais disponiveis
        """
        return self.methods.get("/tribunal/origens");

    def get_detalhes_tribunal(self, sigla_tribunal):
        """
        Retorna os detalhes do tribunal enviado
        :param sigla_tribunal: the acronym of the searched court system
        :return: json contendo os detalhes do tribunal enviado
        """
        return self.methods.get(f"/tribunal/origens/{sigla_tribunal}");