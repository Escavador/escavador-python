from escavador.resources.endpoint import Endpoint


class Legislacao(Endpoint):

    def filtros_busca_legislacao(self):
        """
        Lista de filtros disponíveis para a busca de Legislação
        :return: json
        """
        return self.methods.get("/legislacoes")

    def busca_por_legislation(self, termo, **kwargs):
        """
        Traz a lista paginada dos itens encontrados na busca.
        :param termo: o termo a ser pesquisado
        :keyword arguments:
            **ordena_por**(``orderna-por``) -- modifica a forma como o retorno da busca será ordenado
            **de_data**(``de_data``) -- filtra os resultados com data de julgamento a partir da data informada
            **ate_data**(``ate_data``) -- filtra os resultados com data de julgamento limite até a data informada
            **pagina**(``pagina``) -- lista os itens de uma página
            **filtro**(``filtro``) -- Um dos filtros listados pelo método filtros_busca_legislacao()
        :return: json
        """

        data = {
            'q': termo,
            'ordena_por': kwargs.get('ordena_por'),
            'de_data': kwargs.get('de_data'),
            'ate_data': kwargs.get('ate_data'),
            'pagina': kwargs.get('data'),
            'filtro': kwargs.get('filtro')
        }

        return self.methods.get('/legislacoes/busca', data=data)

    def get_documento_legislacao(self, tipo_documento, id_documento):
        """
        Traz informações sobre um documento de Legislação
        :param tipo_documento: the type of the document
        :param id_documento: the document ID
        :return json
        """

        return self.methods.get(f"/legislacoes/documento/{tipo_documento}/{id_documento}")

    def fragmentos_texto_legislacao(self, tipo_documento, id_documento):
        """
        Traz os fragmentos de uma legislação paginados.
        :param tipo_documento: the type of the document
        :param id_documento: the document ID
        :return: json containing text fragments
        """

        return self.methods.get(f"/legislacoes/pdf/{tipo_documento}/{id_documento}/fragmentos")