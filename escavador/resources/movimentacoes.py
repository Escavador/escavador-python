from escavador.resources.endpoint import Endpoint


class Movimentacao(Endpoint):

    def get(self, id_movimentacao: int) -> dict:
        """
        Retorna uma movimentação pelo seu identificador
        :param id_movimentacao: o ID da movimentação
        :return: dict
        """
        return self.methods.get(f"movimentacoes/{id_movimentacao}")
