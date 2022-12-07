from escavador.resources.helpers.endpoint import Endpoint
from typing import Optional
from datetime import datetime


class Legislacao(Endpoint):

    def filtros_busca_legislacao(self) -> dict:
        """
        Lista de filtros disponíveis para a busca de Legislação
        :return: dict
        """
        return self.methods.get("legislacoes")

    def busca_por_legislacao(self, termo: str, *, ordena_por: Optional[str] = None, de_data: Optional[datetime] = None,
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

        return self.methods.get('legislacoes/busca', data=data)

    def get_documento_legislacao(self, tipo_documento: str, id_documento: int) -> dict:
        """
        Traz informações sobre um documento de Legislação
        :param tipo_documento: O tipo do Documento
        :param id_documento: O ID do documento
        :return dict
        """

        return self.methods.get(f"legislacoes/documento/{tipo_documento}/{id_documento}")

    def fragmentos_texto_legislacao(self, tipo_documento: str, id_documento: int) -> dict:
        """
        Traz os fragmentos de uma legislação paginados.
        :param tipo_documento: O tipo do Documento
        :param id_documento: O ID do documento
        :return: dict
        """

        return self.methods.get(f"legislacoes/pdf/{tipo_documento}/{id_documento}/fragmentos")
