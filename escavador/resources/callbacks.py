from escavador.resources.endpoint import Endpoint


class Callbacks(Endpoint):

    def get_callbacks(self, **kwargs):
        """
        :keyword Arguments:
            **data_maxima*(``date``) -- a data máxima do callback
            **data_maxima**(``date``) -- a data mínima do callback
            **evento**(``string``) -- o evento do callback
            **item_tipo**(``string``) -- o tipo do item do callback e.g: busca_assincrona, monitoramento_tribunal
            , monitoramento_diario
            **item_id**(``int``) -- o id do item do callback, obrigatório se o item_tipo foi enviado
        :return: json
        """

        data = {
            "data_maxima":kwargs.get('data_maxima'),
            "data_minima": kwargs.get('data_minima'),
            "evento": kwargs.get('evento'),
            "item_tipo": kwargs.get('item_tipo'),
            "item_id": kwargs.get('item_id')
        }

        return self.methods.get('callbacks', data=data)
