from escavador.resources.endpoint import Endpoint


class Tribunal(Endpoint):

    def get_sistemas_tribunais_disponiveis(self) -> dict:
        """
        Retorna todos os sistemas de tribunais disponiveis
        :return: dict
        """
        return self.methods.get("tribunal/origens")

    def get_detalhes(self, sigla_tribunal: str) -> dict:
        """
        Retorna os detalhes do tribunal enviado
        :param sigla_tribunal: the acronym of the searched court system
        :return: dict
        """
        return self.methods.get(f"tribunal/origens/{sigla_tribunal}")
