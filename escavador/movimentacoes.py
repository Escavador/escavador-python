from escavador.endpoint import Endpoint


class Movimentacao(Endpoint):

    def get_movimentacao(self, id_movimentacao):
        """
        Retorna uma movimentação pelo seu identificador
        :param id_movimentacao: o ID da movimentação
        :return: json
        """
        return self.methods.get("/movimentacoes/{}".format(id_movimentacao))