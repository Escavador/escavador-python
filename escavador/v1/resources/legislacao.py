from escavador.resources.helpers.endpoint import EndpointV1
from typing import Optional, Dict
from datetime import datetime


class Legislacao(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def filtros_busca_legislacao(cls) -> Dict:
        """
        Lista de filtros disponíveis para a busca de Legislação
        :return: Dict
        """
        return cls.methods.get("legislacoes")

    @classmethod
    def busca_por_legislacao(cls, termo: str, *, ordena_por: Optional[str] = None, de_data: Optional[datetime] = None,
                             ate_data: Optional[datetime] = None, pagina: Optional[int] = None,
                             filtro: Optional[str] = None) -> Dict:
        """
        Traz a lista paginada dos itens encontrados na busca.
        :param filtro: Um dos filtros listados pelo método filtros_busca_jurisprudencia()
        :param pagina: lista os itens de uma página
        :param ate_data: filtra os resultados com data de julgamento limite até a data informada
        :param de_data: filtra os resultados com data de julgamento a partir da data informada
        :param ordena_por: modifica a forma como o retorno da busca será ordenado
        :param termo: o termo a ser pesquisado
        :return: Dict
        """

        params = {
            'q': termo,
            'ordena_por': ordena_por,
            'de_data': de_data.strftime("%Y%m%d") if de_data else None,
            'ate_data': ate_data.strftime("%Y%m%d") if ate_data else None,
            'pagina': pagina,
            'filtro': filtro
        }

        return cls.methods.get('legislacoes/busca', params=params)

    @classmethod
    def get_documento_legislacao(cls, tipo_documento: str, id_documento: int) -> Dict:
        """
        Traz informações sobre um documento de Legislação
        :param tipo_documento: O tipo do Documento
        :param id_documento: O ID do documento
        :return Dict
        """

        return cls.methods.get(f"legislacoes/documento/{tipo_documento}/{id_documento}")

    @classmethod
    def fragmentos_texto_legislacao(cls, tipo_documento: str, id_documento: int) -> Dict:
        """
        Traz os fragmentos de uma legislação paginados.
        :param tipo_documento: O tipo do Documento
        :param id_documento: O ID do documento
        :return: Dict
        """

        return cls.methods.get(f"legislacoes/pdf/{tipo_documento}/{id_documento}/fragmentos")
