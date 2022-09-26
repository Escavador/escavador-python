from escavador.resources.helpers.endpoint import Endpoint


class Tribunal(Endpoint):

    def sistemas_disponiveis(self) -> dict:
        """
        Retorna todos os sistemas de tribunais disponiveis
        :return: dict
        """
        return self.methods.get("tribunal/origens")

    def detalhes(self, sigla_tribunal: str) -> dict:
        """
        Retorna os detalhes do tribunal enviado
        :param sigla_tribunal: A sigla do sistema de tribunal pesquisado
        :return: dict
        """
        return self.methods.get(f"tribunal/origens/{sigla_tribunal}")
