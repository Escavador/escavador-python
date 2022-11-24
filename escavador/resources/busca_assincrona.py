from escavador.resources.helpers.endpoint import Endpoint


class BuscaAssincrona(Endpoint):

    def por_id(self, id: int) -> dict:
        """
        Retorna dados de uma busca assíncrona pelo id
        :param id: o ID da busca assíncrona
        :return: dict
        """
        return self.methods.get(f"async/resultados/{id}")

    def resultados(self) -> dict:
        """
        Consultar todos os resultados das buscas assíncrona
        :return: dict
        :return:
        """
        return self.methods.get("async/resultados")