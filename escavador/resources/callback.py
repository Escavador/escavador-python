from datetime import datetime

from escavador.resources.helpers.endpoint import Endpoint
from typing import Optional

from escavador.resources.helpers.enums import StatusCallback


class Callback(Endpoint):

    def callbacks(self, *, data_maxima: Optional[datetime] = None, data_minima: Optional[datetime] = None,
            evento: Optional[str] = None, item_tipo: Optional[str] = None, item_id: Optional[int] = None,
            status: Optional[StatusCallback]) -> dict:
        """
        Retorna todos os callbacks, de acordo com os filtros enviados
        :param item_id:o id do item do callback, obrigatório se o item_tipo foi enviado
        :param item_tipo: o tipo do item do callback e.g: busca_assincrona, monitoramento_tribunal, monitoramento_diario
        :param evento: o evento do callback
        :param data_minima: a data mínima do callback
        :param data_maxima: a data máxima do callback
        :param status: status do callback
        :return: dict
        """

        data = {
            "data_maxima": data_maxima.strftime("%Y-%m-%d %H:%M:%S") if data_maxima else None,
            "data_minima": data_minima.strftime("%Y-%m-%d %H:%M:%S") if data_minima else None,
            "evento": evento,
            "item_tipo": item_tipo,
            "item_id": item_id,
            "status": status.value
        }

        return self.methods.get('callbacks', data=data)

    def marcarRecebido(self, ids: list) -> dict:
        """
        Marca callbacks como recebidos
        :param ids:lista com ids dos callbacks que serão marcardos como recebidos
        :return: dict
        """

        data = {
            'ids': ids
        }

        return self.methods.post('callbacks/marcar-recebidos',data=data)

    def reenviar(self, id: int) -> dict:
        """
        Reenvia uma callback
        :param id: id do callback
        :return: dict
        """

        return self.methods.post(f'callbacks/{id}/reenviar')