from escavador.resources.helpers.endpoint import Endpoint
from escavador.resources.helpers.documento import Documento
from typing import Optional
from datetime import  datetime


class Jurisprudencia(Endpoint):

    def filtros_busca_jurisprudencia(self) -> dict:
        """
        Lista de filtros disponíveis para a busca de jurisprudências
        :return: dict
        """
        return self.methods.get("jurisprudencias")

    def busca_por_jurisprudencias(self, termo: str, *, ordena_por: Optional[str] = None, de_data: Optional[datetime] = None,
                                  ate_data: Optional[datetime] = None, pagina: Optional[int] = None,
                                  filtro: Optional[str] = None) -> dict:
        """
        Traz a lista paginada dos itens encontrados na busca.
        :param filtro: Um dos filtros listados pelo método filtros_busca_jurisprudencia()
        :param pagina: lista os itens de uma página
        :param ate_data: filtra os resultados com data de julgamento limite até a data informada
        :param de_data: filtra os resultados com data de julgamento a partir da data informada
        :param ordena_por: modifica a forma como o retorno da busca será ordenado
        :param termo: o termo a ser pesquisado
        :return: dict
        """

        data = {
            'q': termo,
            'ordena_por': ordena_por,
            'de_data': de_data.strftime("%Y%m%d") if de_data else None,
            'ate_data': ate_data.strftime("%Y%m%d") if ate_data else None,
            'pagina': pagina,
            'filtro': filtro
        }

        return self.methods.get('jurisprudencias/busca', data=data)

    def get_documento_jurisprudencia(self, tipo_documento: str, id_documento: int) -> dict:
        """
        Traz informações sobre um documento de Jurisprudência em específico
        :param tipo_documento: o tipo de documento
        :param id_documento: o ID do documento
        :return dict
        """

        return self.methods.get(f"jurisprudencias/documento/{tipo_documento}/{id_documento}")

    def download_documento_jurisprudencia(self, tipo_documento: str, id_documento: int, id_arquivo: str, path: str,
                                          nome_arquivo: str) -> dict:
        """
        Retorna, em formato PDF, um documento de jurisprudência
         :param tipo_documento: o tipo de documento
        :param id_documento: o ID do documento
        :param id_arquivo: o ID do arquivo do documento
        :param path: caminho onde o pdf será salvo
        :param nome_arquivo: nome do arquivo a ser criado
        :return: dict
        """

        conteudo = self.methods.get(f"jurisprudencias/pdf/{tipo_documento}/{id_documento}/{id_arquivo}")

        if conteudo['sucesso'] is True:
            return Documento.get_pdf(conteudo, path, nome_arquivo)
        else:
            return conteudo
