from escavador.resources.helpers.endpoint import Endpoint


class Movimentacao(Endpoint):

    def por_id(self, id_movimentacao: int) -> dict:
        """
        Retorna uma movimentação pelo seu identificador
        :param id_movimentacao: o ID da movimentação
        :return: dict
        """
        return self.methods.get(f"movimentacoes/{id_movimentacao}")
