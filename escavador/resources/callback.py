from escavador.resources.helpers.endpoint import Endpoint
from typing import Optional


class Callback(Endpoint):

    def get(self, *, data_maxima: Optional[str] = None, data_minima: Optional[str] = None,
            evento: Optional[str] = None, item_tipo: Optional[str] = None, item_id: Optional[int] = None) -> dict:
        """
        Retorna todos os callbacks, de acordo com os filtros enviados
        :param item_id:o id do item do callback, obrigatório se o item_tipo foi enviado
        :param item_tipo: o tipo do item do callback e.g: busca_assincrona, monitoramento_tribunal, monitoramento_diario
        :param evento: o evento do callback
        :param data_minima: a data mínima do callback
        :param data_maxima a data máxima do callback
        :return: dict
        """

        data = {
            "data_maxima": data_maxima,
            "data_minima": data_minima,
            "evento": evento,
            "item_tipo": item_tipo,
            "item_id": item_id
        }

        return self.methods.get('callbacks', data=data)
