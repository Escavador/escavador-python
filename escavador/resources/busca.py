from __future__ import annotations
from escavador.resources.endpoint import Endpoint
from escavador.exceptions import InvalidParamsException
from escavador.validator import Validator
from typing import Optional


class Busca(Endpoint):

    def get_termo(self, termo: str, tipo_termo: str, *, limit: Optional[int] = None,
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

        available_types = ['t', 'p', 'i', 'pa', 'd', 'en']

        if tipo_termo not in available_types:
            raise InvalidParamsException("Tipo de termo invalido")

        data = {
            'q': termo,
            'qo': tipo_termo,
            'limit': limit,
            'page': page
        }
        return self.methods.get("busca", data=data)

    def get_processo_por_oab(self, estado_oab: str, numero_oab: str | int, *, page: Optional[int] = None) -> dict:
        """
        Busca processos que estão nos Diários Oficiais do Escavador que estão relacionados ao OAB informado
        :param page: número da página
        :param estado_oab: sigla do estado da OAB
        :param numero_oab: número da OAB
        :return: dict
        """

        data = {
            'page': page
        }

        if estado_oab not in Validator.valid_states():
            raise InvalidParamsException("Invalid state")

        return self.methods.get(f"oab/{estado_oab}/{numero_oab}/processos", data=data)

    def get_processo(self, id_processo: int) -> dict:
        """
        Retorna um processo pelo seu identificador no Escavador.
        :param id_processo: o ID do processo
        :return: dict
        """

        return self.methods.get(f"processos/{id_processo}")

    def get_movimentacao_processo(self, id_processo: int, *, limit: Optional[int] = None,
                                  page: Optional[int] = None) -> dict:
        """
        Retorna as movimentações de um Processo pelo identificador do processo no Escavador.
        :param page: número da página
        :param limit: limita a quantidade de registros retornados
        :param id_processo:  o ID do processo
        :return: dict
        """

        data = {
            'limit': limit,
            'page': page
        }

        return self.methods.get(f"processos/{id_processo}/movimentacoes", data=data)

    def get_processo_por_numero_unico(self, numero_unico: str, *, match_exato: Optional[bool] = None) -> dict:
        """
        Busca processos que estão nos Diários Oficiais do Escavador. e contenham o número único informado.
        :param match_exato: a busca será feita pelo número inteiro do processo pesquisado.
        :param numero_unico: número único do processo
        :return: dict
        """

        data = {
            'match_exato': match_exato
        }

        return self.methods.get(f"processos/numero/{numero_unico}", data=data)

    def get_envolvidos_processo(self, id_processo: int, *, limit: Optional[int] = None,
                                page: Optional[int] = None) -> dict:
        """
       Retorna os envolvidos de um Processo pelo identificador do processo no Escavador.
        :param id_processo:  o ID do processo
        :param page: número da página
        :param limit: limita a quantidade de registros retornados
        :return: dict
        """

        data = {
            'limit': limit,
            'page': page
        }

        return self.methods.get(f"processos/{id_processo}/envolvidos", data=data)
