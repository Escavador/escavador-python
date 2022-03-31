from escavador.resources.endpoint import Endpoint


class Movimentacao(Endpoint):

    def get_movimentacao(self, id_movimentacao):
        """
        Retorna uma movimentação pelo seu identificador
        :param id_movimentacao: o ID da movimentação
        :return: json
        """
        return self.methods.get(f"movimentacoes/{id_movimentacao}")