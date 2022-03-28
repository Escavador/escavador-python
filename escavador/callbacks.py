from escavador.method import Method


class Callbacks(object):

    def __init__(self):
        self.methods = Method

    def get_callbacks(self, **kwargs):
        """
        :keyword Arguments:
            **data_maxima*(``date``) -- the max date of the callback \n
            **data_maxima**(``date``) -- the min date of the callback \n
            **evento**(``string``) -- the event related to the callback \n
            **item_tipo**(``string``) -- the type of the callback item. e.g: busca_assincrona, monitoramento_tribunal, monitoramento_diario
            **item_id**(``int``) -- the id of the callback item, required if the item_tipo was sent
        :param kwargs:
        :return: json containing all the user's callbacks, based on the sent filters
        """

        data = {
            "data_maxima":kwargs.get('data_maxima'),
            "data_minima": kwargs.get('data_minima'),
            "evento": kwargs.get('evento'),
            "item_tipo": kwargs.get('item_tipo'),
            "item_id": kwargs.get('item_id')
        }

        return self.methods.get('/callbacks', data=data)
