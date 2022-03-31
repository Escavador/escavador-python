from escavador.resources.endpoint import Endpoint


class DiarioOficial(Endpoint):

    def get_origens(self):
        """
        Retorna as origens de todos os diários disponiveis no Escavador.
        :return: json
        """
        return self.methods.get("origens")

    def get_pagina_diario(self, id_diario, **kwargs):
        """
        Retorna uma página específica do Diário Oficial pelo seu identificador no Escavador.
        :param id_diario: o ID do diario oficial
        :keyword arguments:
            **page**(``int``) -- número da página do diário oficial
        :return: json
        """
        data = kwargs.get('page')

        return self.methods.get(f"diarios/{id_diario}", data=data)

    def download_pdf_pagina_diario(self, id_diario, page):
        """
        Retorna em formato PDF, uma página do Diário Oficial pelo seu identificador
        :param id_diario: o ID do diario oficial
        :param page: número da página do diário oficial
        :return: pdf com a página do diario
        """
        return self.methods.get(f"diarios/{id_diario}/pdf/pagina/{page}/baixar")