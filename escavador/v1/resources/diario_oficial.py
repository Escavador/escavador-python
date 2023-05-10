from escavador.resources.helpers.endpoint import EndpointV1
from escavador.resources.helpers.documento import Documento
from typing import Optional, Dict


class DiarioOficial(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def origens(cls) -> Dict:
        """
        Retorna as origens de todos os diários disponiveis no Escavador.
        :return: Dict
        """
        return cls.methods.get("origens")

    @classmethod
    def pagina(cls, id_diario: int, *, page: Optional[int] = None) -> Dict:
        """
        Retorna uma página específica do Diário Oficial pelo seu identificador no Escavador.
        :param id_diario: o ID do diario oficial
        :param page: número da página do diário oficial
        :return: Dict
        """
        data = {
            "page": page
        }

        return cls.methods.get(f"diarios/{id_diario}", data=data)

    @classmethod
    def download_pdf_pagina(cls, id_diario: int, page: int, path: str, nome_arquivo: str) -> Dict:
        """
        Retorna em formato PDF, uma página do Diário Oficial pelo seu identificador
        :param nome_arquivo:nome para o arquivo baixado
        :param path: diretorio onde o arquivo será salvo
        :param id_diario: o ID do diario oficial
        :param page: número da página do diário oficial
        :return: Dict
        """
        conteudo = cls.methods.get(f"diarios/{id_diario}/pdf/pagina/{page}/baixar")

        if type(conteudo) is dict:
            return conteudo
        else:
            return Documento.get_pdf(conteudo, path, nome_arquivo)
