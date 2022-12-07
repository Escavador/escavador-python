from escavador.resources.helpers.endpoint import Endpoint
from escavador.resources.helpers.documento import Documento
from typing import Optional


class DiarioOficial(Endpoint):

    def origens(self) -> dict:
        """
        Retorna as origens de todos os diários disponiveis no Escavador.
        :return: dict
        """
        return self.methods.get("origens")

    def pagina(self, id_diario: int, *, page: Optional[int] = None) -> dict:
        """
        Retorna uma página específica do Diário Oficial pelo seu identificador no Escavador.
        :param id_diario: o ID do diario oficial
        :param page: número da página do diário oficial
        :return: dict
        """
        data = {
            "page": page
        }

        return self.methods.get(f"diarios/{id_diario}", data=data)

    def download_pdf_pagina(self, id_diario: int, page: int, path: str, nome_arquivo: str) -> dict:
        """
        Retorna em formato PDF, uma página do Diário Oficial pelo seu identificador
        :param nome_arquivo:nome para o arquivo baixado
        :param path: diretorio onde o arquivo será salvo
        :param id_diario: o ID do diario oficial
        :param page: número da página do diário oficial
        :return: dict
        """
        conteudo = self.methods.get(f"diarios/{id_diario}/pdf/pagina/{page}/baixar")

        if conteudo['sucesso'] is True:
            return Documento.get_pdf(conteudo, path, nome_arquivo)
        else:
            return conteudo
