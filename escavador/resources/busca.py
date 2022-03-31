from escavador.resources.endpoint import Endpoint
from escavador.exceptions import InvalidParamsException


class Busca(Endpoint):

    def get_termo(self, termo, tipo_termo, **kwargs):
        """
        Pesquisa um termo no escavador
        :param termo: o termo a ser pesquisado
        :param tipo_termo: Tipo da entidade a ser pesquisada(*t* - todos os tipos, *p* -- apenas pessoas,
         *i* -- apenas instituições, *pa* -- apenas patentes, *d* -- apenas diários oficiais,
          *en* -- apenas pessoas e instituições envolvidas em processos)
        :keyword Arguments:
            **limit*(``int``) -- limita a quantidade de registros retornados
            **page**(``ìnt``) -- número da página
        :return:json
        """

        available_types = ['t', 'p', 'i', 'pa', 'd', 'en']

        if tipo_termo not in available_types:
            raise InvalidParamsException("Invalid word type")

        data = {
            'q': termo,
            'qo': tipo_termo,
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }

        return self.methods.get("/busca", data=data)

    def get_processo_por_oab(self, estado_oab, numero_oab, **kwargs):
        """
        Busca processos que estão nos Diários Oficiais do Escavador que estão relacionados ao OAB informado
        :param estado_oab: sigla do estado da OAB
        :param numero_oab: número da OAB
        :keyword Arguments:
             **page**(``ìnt``) -- número da página
        :return: json
        """

        data = {
            'page': kwargs.get('page')
        }

        if estado_oab not in self.states:
            raise InvalidParamsException("Invalid state")

        return self.methods.get(f"/oab/{estado_oab}/{numero_oab}/processos", data=data)

    def get_processo(self, id_processo):
        """
        Retorna um processo pelo seu identificador no Escavador.
        :param id_processo: o ID do processo
        :return: json
        """

        return self.methods.get(f"/processos/{id_processo}")

    def get_movimentacao_processo(self, id_processo, **kwargs):
        """
        Retorna as movimentações de um Processo pelo identificador do processo no Escavador.
        :param id_processo:  o ID do processo
        :keyword Arguments:
            **limit*(``int``) -- limita a quantidade de registros retornados
            **page**(``ìnt``) -- número da página
        :return: json
        """

        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }

        return self.methods.get(f"/processos/{id_processo}/movimentacoes", data=data)

    def get_processo_por_numero_unico(self, numero_unico, **kwargs):
        """
        usca processos que estão nos Diários Oficiais do Escavador. e contenham o número único informado.
        :param numero_unico: número único do processo
        :keyword Arguments:
              **match_exato**(``boolean``) -- a busca será feita pelo número inteiro do processo pesquisado.
        :return: json
        """

        data = {
            'match_exato': kwargs.get('match_exato')
        }

        return self.methods.get(f"/processos/numero/{numero_unico}", data=data)

    def get_envolvidos_processo(self, id_processo, **kwargs):
        """
       Retorna os envolvidos de um Processo pelo identificador do processo no Escavador.
        :param id_processo:  o ID do processo
        :keyword arguments:
            **limit*(``int``) -- limita a quantidade de registros retornados
            **page**(``ìnt``) -- número da página
        :return: json
        """

        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }

        return self.methods.get(f"/processos/{id_processo}/envolvidos", data=data)





