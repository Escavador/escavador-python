import re
from enum import Enum

from escavador.resources.helpers.endpoint import Endpoint
from escavador.resources.helpers.enums import Ordem
from typing import Optional, Dict, List, Union


class BuscaProcesso(Endpoint):
    class CriterioOrdenacao(Enum):
        ULTIMA_MOVIMENTACAO = "data_ultima_movimentacao"
        INICIO = "data_inicio"

    def __init__(self):
        super().__init__(api_version=2)

    def por_numero(self, numero_cnj: str, **kwargs) -> Dict:
        """
        Retorna os dados de um processo pelo seu número único do CNJ.
        :param numero_cnj: o número único do CNJ do processo
        :return: Dict

        >>> BuscaProcesso().por_numero("0000000-00.0000.0.00.0000") # doctest: +SKIP
        """
        data = kwargs

        return self.methods.get(f"processos/numero_cnj/{numero_cnj}", data=data)

    def movimentacoes(self, numero_cnj: str, qtd: int = 100, **kwargs) -> Dict:
        """
        Retorna as movimentações de um processo pelo seu número único do CNJ.
        :param numero_cnj: o número único do CNJ do processo
        :param qtd: quantidade desejada de movimentações a ser retornada pela query
        :return:

        >>> BuscaProcesso().movimentacoes("0000000-00.0000.0.00.0000") # doctest: +SKIP

        >>> BuscaProcesso().movimentacoes("0000000-00.0000.0.00.0000", qtd=10) # doctest: +SKIP
        """
        data = kwargs

        return self.methods.get(f"processos/numero_cnj/{numero_cnj}/movimentacoes", data=data)

    def por_nome(self,
                 nome: str,
                 ordena_por: Optional[CriterioOrdenacao] = None,
                 ordem: Optional[Ordem] = None,
                 tribunais: Optional[List[str]] = None,
                 qtd: int = 100,
                 **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma pessoa ou empresa a partir do seu nome.
        :param nome: o nome da pessoa ou empresa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query

        >>> BuscaProcesso().por_nome("Escavador Engenharia e Construcoes Ltda",
        ...                          ordena_por=BuscaProcesso.CriterioOrdenacao.INICIO,
        ...                          ordem=Ordem.DESC,
        ...                          tribunais=['TJBA', 'TRF1'],
        ...                          qtd=1) # doctest: +SKIP

        >>> BuscaProcesso().por_nome("Escavador Engenharia e Construcoes Ltda") # doctest: +SKIP
        """
        return self.por_envolvido(nome=nome,
                                  ordena_por=ordena_por,
                                  ordem=ordem,
                                  tribunais=tribunais,
                                  qtd=qtd,
                                  **kwargs)

    def por_cpf(self,
                cpf: str,
                ordena_por: Optional[CriterioOrdenacao] = None,
                ordem: Optional[Ordem] = None,
                tribunais: Optional[List[str]] = None,
                qtd: int = 100,
                **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma pessoa a partir de seu CPF.
        :param cpf: o CPF da pessoa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query

        >>> BuscaProcesso().por_cpf("12345678999",
        ...                         ordena_por=BuscaProcesso.CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                         ordem=Ordem.ASC,
        ...                         tribunais=['STF'],
        ...                         qtd=200) # doctest: +SKIP

        >>> BuscaProcesso().por_cpf("123.456.789-99") # doctest: +SKIP
        """
        return self.por_envolvido(cpf_cnpj=cpf,
                                  ordena_por=ordena_por,
                                  ordem=ordem,
                                  tribunais=tribunais,
                                  qtd=qtd,
                                  **kwargs)

    def por_cnpj(self,
                 cnpj: str,
                 ordena_por: Optional[CriterioOrdenacao] = None,
                 ordem: Optional[Ordem] = None,
                 tribunais: Optional[List[str]] = None,
                 qtd: int = 100,
                 **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma instituição a partir de seu CNPJ.
        :param cnpj: o CNPJ da instituição
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query

        >>> BuscaProcesso().por_cnpj("07.838.351/0021.60",
        ...                          ordena_por=BuscaProcesso.CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                          ordem=Ordem.ASC,
        ...                          tribunais=['TJBA', 'TRF1'],
        ...                          qtd=1) # doctest: +SKIP

        >>> BuscaProcesso().por_cnpj("07838351002160") # doctest: +SKIP
        """
        return self.por_envolvido(cpf_cnpj=cnpj,
                                  ordena_por=ordena_por,
                                  ordem=ordem,
                                  tribunais=tribunais,
                                  qtd=qtd,
                                  **kwargs)

    def por_envolvido(self,
                      cpf_cnpj: Optional[str] = None,
                      nome: Optional[str] = None,
                      ordena_por: Optional[CriterioOrdenacao] = None,
                      ordem: Optional[Ordem] = None,
                      tribunais: Optional[List[str]] = None,
                      qtd: int = 100,
                      **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma pessoa ou instituição a partir de seu nome e/ou CPF/CNPJ.

        Caso seja necessário múltiplos requests para obter a quantidade de processos desejada e algum
        erro ocorra em um request intermediário, a função retorna todos os processos obtidos até o
        momento com o o status code do erro ocorrido nesse último request.

        :param nome: o nome da pessoa ou instituição. Obrigatório se não for informado o CPF/CNPJ
        :param cpf_cnpj: o CPF/CNPJ da pessoa ou instituição. Obrigatório se não for informado o nome
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query


        >>> BuscaProcesso().por_envolvido(nome='Escavador Engenharia e Construcoes Ltda',
        ...                               ordena_por=BuscaProcesso.CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                               ordem=Ordem.ASC,
        ...                               tribunais=['TJBA'],
        ...                               qtd=1) # doctest: +SKIP

        >>> BuscaProcesso().por_envolvido(cpf_cnpj="07.838.351/0021.60") # doctest: +SKIP
        """
        data = {
            'nome': nome,
            'cpf_cnpj': cpf_cnpj,
            'tribunais': tribunais,
        }

        params = {
            'ordena_por': ordena_por.value if ordena_por else None,
            'ordem': ordem.value if ordem else None,
        }

        current_response = self.methods.get(f"envolvido/processos", data=data, params=params, **kwargs)
        while 0 < len(current_response['resposta'].get('items', [])) < qtd:
            cursor = current_response['resposta']['links']['next']
            if not cursor:
                break

            next_response = self.__get_more(cursor, **kwargs)
            next_items = next_response['resposta'].get('items')
            if not next_items:
                current_response['http_status'] = next_response['http_status']
                current_response['success'] = next_response['success']
                break

            current_response['resposta']['items'].extend(next_items)

            next_cursor = next_response['resposta']['links']['next']
            if not next_cursor:
                break

            current_response['resposta']['links']['next'] = next_cursor

        return self.__selecionar_alguns(current_response, qtd)

    def por_oab(self,
                numero: Union[str, int],
                estado: str,
                ordena_por: Optional[CriterioOrdenacao] = None,
                ordem: Optional[Ordem] = None,
                qtd: int = 100,
                **kwargs
                ) -> Dict:
        """
        Retorna os processos de um advogado a partir de sua carteira da OAB.
        :param numero: o número da OAB
        :param estado: o estado de origem da OAB
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param qtd: quantidade desejada de processos a ser retornada pela query

        >>> BuscaProcesso().por_oab(1234, "AC") # doctest: +SKIP

        >>> BuscaProcesso().por_oab(numero="123456",
        ...                         estado="SP",
        ...                         ordena_por=BuscaProcesso.CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                         ordem=Ordem.DESC,
        ...                         qtd=1) # doctest: +SKIP
        """
        data = {
            'oab_numero': f"{numero}",
            'oab_estado': estado,
        }
        params = {
            'ordena_por': ordena_por.value if ordena_por else None,
            'ordem': ordem.value if ordem else None,
        }
        return self.methods.get(f"advogado/processos", data=data, params=params)

    def __get_more(self, cursor: str, **kwargs) -> Dict:
        """Consome um cursor para obter os próximos resultados de uma busca
        :param cursor: o cursor a ser consumido
        :return: um dicionário com a resposta da requisição
        """
        endpoint_cursor = re.sub(r".*/api/v\d/", "", cursor)
        return self.methods.get(endpoint_cursor, **kwargs)

    @staticmethod
    def __selecionar_alguns(resposta: Dict, qtd: int) -> Dict:
        """Seleciona os itens de uma resposta de acordo com a quantidade desejada

        :param resposta: a resposta a ser filtrada
        :param qtd: a quantidade de itens desejada
        :return: a resposta com a quantidade de itens desejada
        """
        if 'items' in resposta['resposta']:
            resposta['resposta']['items'] = resposta['resposta']['items'][:qtd]
        return resposta
