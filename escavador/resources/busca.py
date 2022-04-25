from escavador.resources.helpers.endpoint import Endpoint
from typing import Optional
from escavador.resources.helpers.enums import TiposTermo


class Busca(Endpoint):

    def busca_termo(self, termo: str, tipo_termo: TiposTermo, *, limit: Optional[int] = None,
                    page: Optional[int] = None) -> dict:
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
        :return: dict
        """

        data = {
            'q': termo,
            'qo': tipo_termo.value,
            'limit': limit,
            'page': page
        }
        return self.methods.get("busca", data=data)
