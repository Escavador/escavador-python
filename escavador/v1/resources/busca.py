from escavador.resources.helpers.endpoint import EndpointV1
from typing import Optional, Dict
from escavador.resources.helpers.enums import TiposTermo


class Busca(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def busca_termo(cls, termo: str, tipo_termo: TiposTermo, *, limit: Optional[int] = None,
                    page: Optional[int] = None) -> Dict:
        """
        Pesquisa um termo no escavador
        :param page: número da página
        :param limit: limita a quantidade de registros retornados
        :param termo: o termo a ser pesquisado
        :param tipo_termo: Tipo da entidade a ser pesquisada(
        *t* - todos os tipos
        *p* -- apenas pessoas
        *i* -- apenas instituições
        *pa* -- apenas patentes
        *d* -- apenas diários oficiais
        *en* -- apenas pessoas e instituições envolvidas em processos)
        :return: Dict
        """

        data = {
            'q': termo,
            'qo': tipo_termo.value,
            'limit': limit,
            'page': page
        }
        return cls.methods.get("busca", data=data)
