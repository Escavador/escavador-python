from escavador.method import Method


class Legislation():

    def __init__(self):
        self.methods = Method()

    def filters_to_legislation_search(self):
        """
        Show all the legislation filters available
        :return: a json containing all available filters
        """
        return self.methods.get("/legislacoes")

    def search_by_legislation(self, word, **kwargs):
        """
        Return a paginated list with the items found
        :param word: the word to be searched
        :keyword arguments:
            **ordena_por**(``orderna-por``) -- the type of sorting that will be returned
            **de_data**(``de_data``) -- the starting date limit of the search
            **ate_data**(``ate_data``) -- the ending date limit of the search
            **pagina**(``pagina``) -- select the page from the paginated result
            **filtro**(``filtro``) -- a filter from the available filter from the method filters_to_legislation_search()
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

        return self.methods.get('/legislacoes/busca', data=data)

    def get_legislation_document(self, document_type, document_id):
        """
        Return a legislation document based on sent the type and id
        :param document_type: the type of the document
        :param document_id: the document ID
        :return json containing the document and related documents
        """

        return self.methods.get("/legislacoes/documento/{}/{}".format(document_type, document_id))

    def legislation_text_fragment(self, document_type, document_id):
        """
         Return paginated text fragments from a legislation document
        :param document_type: the type of the document
        :param document_id: the document ID
        :return: json containing text fragments
        """

        return self.methods.get("/legislacoes/pdf/{}/{}/fragmentos".format(document_type, document_id))