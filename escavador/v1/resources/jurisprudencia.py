from escavador.resources.helpers.endpoint import EndpointV1
from escavador.resources.helpers.documento import Documento
from typing import Optional, Dict, List
from datetime import datetime


class Jurisprudencia(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def filtros_busca_jurisprudencia(cls) -> Dict:
        """
        Lista de filtros disponíveis para a busca de jurisprudências,
        Para cada item da lista de filtros, o campo filtro representa a chave (key) da query.
        No campo opcoes, listamos todas as opções de valor para aquele filtro, e, para cada opção,
         o campo valor representa o valor (value) da query.
        :return: Dict
        """
        return cls.methods.get("jurisprudencias")

    @classmethod
    def busca_por_jurisprudencias(cls, termo: str, *, ordena_por: Optional[str] = None, de_data: Optional[datetime] = None,
                                  ate_data: Optional[datetime] = None, pagina: Optional[int] = None,
                                  filtros: Optional[List[Dict]] = None) -> Dict:
        """
        Traz a lista paginada dos itens encontrados na busca.
        :param filtros: filtros listados pelo método filtros_busca_jurisprudencia()
        :param pagina: lista os itens de uma página
        :param ate_data: filtra os resultados com data de julgamento limite até a data informada
        :param de_data: filtra os resultados com data de julgamento a partir da data informada
        :param ordena_por: modifica a forma como o retorno da busca será ordenado
        :param termo: o termo a ser pesquisado
        :return: Dict
        """

        data = {
            'q': termo,
            'ordena_por': ordena_por,
            'de_data': de_data.strftime("%Y%m%d") if de_data else None,
            'ate_data': ate_data.strftime("%Y%m%d") if ate_data else None,
            'pagina': pagina,
        }

        if filtros:
            for filtro in filtros:
                data.update(filtro)

        return cls.methods.get('jurisprudencias/busca', data=data)

    @classmethod
    def get_documento_jurisprudencia(cls, tipo_documento: str, id_documento: int) -> Dict:
        """
        Traz informações sobre um documento de Jurisprudência em específico
        :param tipo_documento: o tipo de documento
        :param id_documento: o ID do documento
        :return Dict
        """

        return cls.methods.get(f"jurisprudencias/documento/{tipo_documento}/{id_documento}")

    @classmethod
    def download_documento_jurisprudencia(cls, tipo_documento: str, id_documento: int, id_arquivo: str, path: str,
                                          nome_arquivo: str) -> Dict:
        """
        Retorna, em formato PDF, um documento de jurisprudência
         :param tipo_documento: o tipo de documento
        :param id_documento: o ID do documento
        :param id_arquivo: o ID do arquivo do documento
        :param path: caminho onde o pdf será salvo
        :param nome_arquivo: nome do arquivo a ser criado
        :return: Dict
        """

        conteudo = cls.methods.get(f"jurisprudencias/pdf/{tipo_documento}/{id_documento}/{id_arquivo}")

        if conteudo['sucesso'] is True:
            return Documento.get_pdf(conteudo, path, nome_arquivo)
        else:
            return conteudo
