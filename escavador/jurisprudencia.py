from escavador.endpoint import Endpoint


class Jurisprudencia(Endpoint):

    def filtros_busca_jurisprudencia(self):
        """
        Lista de filtros disponíveis para a busca de jurisprudências
        :return: json
        """
        return self.methods.get("/jurisprudencias")

    def busca_por_jurisprudencias(self, termo, **kwargs):
        """
        Traz a lista paginada dos itens encontrados na busca.
        :param termo: o termo a ser pesquisado
        :keyword arguments:
            **ordena_por**(``orderna_por``) -- modifica a forma como o retorno da busca será ordenado
            **de_data**(``de_data``) -- filtra os resultados com data de julgamento a partir da data informada
            **ate_data**(``ate_data``) -- filtra os resultados com data de julgamento limite até a data informada
            **pagina**(``pagina``) -- lista os itens de uma página
            **filtro**(``filtro``) -- Um dos filtros listados pelo método filtros_busca_jurisprudencia()
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

        return self.methods.get('/jurisprudencias/busca', data=data)

    def get_documento_jurisprudencia(self, tipo_documento, id_documento):
        """
        Traz informações sobre um documento de Jurisprudência em específico
        :param tipo_documento: o tipo de documento
        :param id_documento: o ID do documento
        :return json
        """

        return self.methods.get("/jurisprudencias/documento/{}/{}".format(tipo_documento, id_documento))

    def download_jurisprudence_document(self, tipo_documento, id_documento, id_arquivo):
        """
        Retorna, em formato PDF, um documento de jurisprudência
         :param tipo_documento: o tipo de documento
        :param id_documento: o ID do documento
        :param id_arquivo: o ID do arquivo do documento
        :return: pdf do documento de jurisprudencia
        """

        return self.methods.get("/jurisprudencias/pdf/{}/{}/{}".format(tipo_documento, id_documento, id_arquivo))