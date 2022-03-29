from escavador.endpoint import Endpoint
from escavador.exceptions import InvalidParamsException


class AsyncSearch(Endpoint):

    def get_lawsuit(self, unique_number, **kwargs):
        """
        Create an async search for the unique number, and search  in the court's sites
        :param unique_number: the unique number
        :keyword arguments:
            **send_callback**(``boolean``) -- option to send a callback with the search result
            **wait**(``boolean``) -- option to wait for the search result
            **autos**(``boolean``) -- option to return the procedural records of the lawsuit
            **usuario**(``string``) -- the lawyer user to the court site, required if autos == True
            **senha**(``string``) -- the lawyer password to the court site, required if autos == True
            **origem**(``string``) -- acronym from the source court of the lawsuit, used to force the search in
            a different court
        :return: json containing the search result or the search
        """

        data = {
            'send_callback': kwargs.get('send_callback'),
            'wait': kwargs.get('wait'),
            'autos': kwargs.get('autos'),
            'usuario': kwargs.get('usuario'),
            'senha':kwargs.get('senha'),
            'origem': kwargs.get('origem')
        }

        return self.methods.post("/processo-tribunal/{}/async".format(unique_number), data=data)

    def get_lawsuit_by_name(self, source, name, **kwargs):
        """
        Create an async search in the source court based on the sent name
        :param source: the court where the name will be searched
        :param name: the name that will be searched
        :keyword Arguments:
            **send_callback**(``boolean``) -- option to send a callback with the search result
            **wait**(``boolean``) -- option to wait for the search result
            **permitir_parcial**(``boolean``) -- option to not make the search in all court systems
        :return: json containing the search result or the search
        """

        data = {
            'nome': name,
            'permitir_parcial': kwargs.get('permitir_parcial'),
            'send_callback': kwargs.get('send_callback'),
            'wait': kwargs.get('wait')
        }

        return self.methods.post("/tribunal/{}/busca-por-nome/async".format(source), data=data)

    def get_lawsuit_by_document(self, source, document, **kwargs):
        """
        Create an async search in the source court based on the sent document
        :param source: the court where the document will be searched
        :param document: the document that will be searched
        :keyword Arguments:
            **send_callback**(``boolean``) -- option to send a callback with the search result
            **wait**(``boolean``) -- option to wait for the search result
            **permitir_parcial**(``boolean``) -- option to not make the search in all court systems
        :return: json containing the search result or the search
        """

        data = {
            'numero_documento': document,
            'permitir_parcial': kwargs.get('permitir_parcial'),
            'send_callback': kwargs.get('send_callback'),
            'wait': kwargs.get('wait')
        }

        return self.methods.post("/tribunal/{}/busca-por-documento/async".format(source), data=data)

    def get_lawsuit_by_oab(self, source, oab_number, oab_state , **kwargs):
        """
        Create an async search in the source court based on the sent oab
        :param source: the court where the oab will be searched
        :param oab_number: the oab number that will be searched
        :param oab_state: the state of the oab sent
        :keyword Arguments:
            **send_callback**(``boolean``) -- option to send a callback with the search result
            **wait**(``boolean``) -- option to wait for the search result
            **permitir_parcial**(``boolean``) -- option to not make the search in all court systems
        :return: json containing the search result or the search
        """

        data = {
            'numero_oab': oab_number,
            'estado_oab': oab_state,
            'permitir_parcial': kwargs.get('permitir_parcial'),
            'send_callback': kwargs.get('send_callback'),
            'wait': kwargs.get('wait')
        }

        return self.methods.post("/tribunal/{}/busca-por-oab/async".format(source), data=data)

    def multi_search(self, search_type, courts, **kwargs):
        """
        Create searches of the same type for all the court sent
        :param courts: the courts where the search will be performed
        :param search_type: the tipe of search, available types: busca_por_nome, busca_por_documento, busca_por_oab
        :keyword Arguments:
            **send_callback**(``boolean``) -- option to send a callback with the search result
            **numero_oab**(``string``) -- the oab number that will be searched
            **estado_oab**(``string``) -- the state of the oab sent
            **numero_documento**(``string``) -- the document that will be searched
            **name**(``string``) -- the name that will be searched
        :return:json containing the search
        """

        available_types = ['busca_por_nome', 'busca_por_documento', 'busca_por_oab']

        if search_type not in available_types:
            raise InvalidParamsException

        data = {
            'tipo': search_type,
            'tribunais': courts,
            'nome': kwargs.get('nome'),
            'numero_documento': kwargs.get('numero_documento'),
            'numero_oab': kwargs.get('numero_oab'),
            'estado_oab': kwargs.get('estado_oab')
        }

        return self.methods.post("/tribunal/async/lote", data=data)

    def get_all_search_results(self):
        """
        Return all the async searches results
        :return: json containing all the async searches
        """

        return self.methods.get('/async/resultados')

    def get_search_result(self, search_id):
        """
        Return a specific async search result
        :return: json containing the search result
        """

        return self.methods.get('/async/resultados/{}'.format(search_id))



