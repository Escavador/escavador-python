from escavador.method import Method


class Jurisprudence(object):

    def __init__(self):
        self.methods = Method()

    def filters_to_jurisprudence_search(self):
        """
        Show all the jurisprudence filters available
        :return: a json containing all available filters
        """
        return self.methods.get("/jurisprudencias")

    def search_by_jurisprudence(self, word, **kwargs):
        """
        Return a paginated list with the items found
        :param word: the word to be searched
        :keyword arguments:
            **ordena_por**(``orderna-por``) -- the type of sorting that will be returned
            **de_data**(``de_data``) -- the starting date limit of the search
            **ate_data**(``ate_data``) -- the ending date limit of the search
            **pagina**(``pagina``) -- select the page from the paginated result
            **filtro**(``filtro``) -- a filter from the available filter from the method filters_to_jurisprudence_search()
        :return: a json containing the result of the seach
        """

        data = {
            'q': word,
            'ordena_por': kwargs.get('ordena_por'),
            'de_data': kwargs.get('de_data'),
            'ate_data': kwargs.get('ate_data'),
            'pagina': kwargs.get('data'),
            'filtro': kwargs.get('filtro')
        }

        return self.methods.get('/jurisprudencias/busca', data=data)

    def get_jurisprudence_document(self, document_type, document_id):
        """
        Return a jurisprudence document based on sent the type and id
        :param document_type: the type of the document
        :param document_id: the document ID
        :return json containing the document and related documents
        """

        return self.methods.get("/jurisprudencias/documento/{}/{}".format(document_type, document_id))

    def download_jurisprudence_document(self, document_type, document_id, file_id):
        """
        Download a pdf of a jurisprudence document
        :param document_type: the type of the document
        :param document_id: the document ID
        :param file_id: the document file ID
        :return: pdf of the found document
        """

        return self.methods.get("/jurisprudencias/pdf/{}/{}/{}".format(document_type, document_id, file_id))