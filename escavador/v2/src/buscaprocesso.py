from enum import Enum

from escavador.resources.helpers.endpoint import Endpoint
from escavador.resources.helpers.enums import Ordem
from typing import Optional, Dict, List, Union


class BuscaProcesso(Endpoint):
    class Ordenacao(Enum):
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

    def movimentacoes(self, numero_cnj: str, **kwargs) -> Dict:
        """
        Retorna as movimentações de um processo pelo seu número único do CNJ.
        :param numero_cnj: o número único do CNJ do processo
        :return:

        >>> BuscaProcesso().movimentacoes("0000000-00.0000.0.00.0000") # doctest: +SKIP
        """
        data = kwargs

        return self.methods.get(f"processos/numero_cnj/{numero_cnj}/movimentacoes", data=data)

    def por_nome(self,
                 nome: str,
                 ordena_por: Optional[Ordenacao] = None,
                 ordem: Optional[Ordem] = None,
                 tribunais: Optional[List[str]] = None,
                 **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma pessoa ou empresa a partir do seu nome.
        :param nome: o nome da pessoa ou empresa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca

        >>> BuscaProcesso().por_nome("Escavador Engenharia e Construcoes Ltda",
        ...                          ordena_por=BuscaProcesso.Ordenacao.INICIO,
        ...                          ordem=Ordem.DESC,
        ...                          tribunais=['TJBA', 'TRF1']) # doctest: +SKIP

        >>> BuscaProcesso().por_nome("Escavador Engenharia e Construcoes Ltda") # doctest: +SKIP
        """
        return self.por_envolvido(nome=nome, ordena_por=ordena_por, ordem=ordem, tribunais=tribunais, **kwargs)

    def por_cpf(self,
                cpf: str,
                ordena_por: Optional[Ordenacao] = None,
                ordem: Optional[Ordem] = None,
                tribunais: Optional[List[str]] = None,
                **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma pessoa a partir de seu CPF.
        :param cpf: o CPF da pessoa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca

        >>> BuscaProcesso().por_cpf("12345678999",
        ...                         ordena_por=BuscaProcesso.Ordenacao.ULTIMA_MOVIMENTACAO,
        ...                         ordem=Ordem.ASC,
        ...                         tribunais=['STF']) # doctest: +SKIP

        >>> BuscaProcesso().por_cpf("123.456.789-99") # doctest: +SKIP
        """
        return self.por_envolvido(cpf_cnpj=cpf, ordena_por=ordena_por, ordem=ordem, tribunais=tribunais, **kwargs)

    def por_cnpj(self,
                 cnpj: str,
                 ordena_por: Optional[Ordenacao] = None,
                 ordem: Optional[Ordem] = None,
                 tribunais: Optional[List[str]] = None,
                 **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma instituição a partir de seu CNPJ.
        :param cnpj: o CNPJ da instituição
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca

        >>> BuscaProcesso().por_cnpj("07.838.351/0021.60",
        ...                          ordena_por=BuscaProcesso.Ordenacao.ULTIMA_MOVIMENTACAO,
        ...                          ordem=Ordem.ASC,
        ...                          tribunais=['TJBA', 'TRF1']) # doctest: +SKIP

        >>> BuscaProcesso().por_cnpj("07838351002160") # doctest: +SKIP
        """
        return self.por_envolvido(cpf_cnpj=cnpj, ordena_por=ordena_por, ordem=ordem, tribunais=tribunais, **kwargs)

    def por_envolvido(self,
                      cpf_cnpj: Optional[str] = None,
                      nome: Optional[str] = None,
                      ordena_por: Optional[Ordenacao] = None,
                      ordem: Optional[Ordem] = None,
                      tribunais: Optional[List[str]] = None,
                      **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma pessoa ou instituição a partir de seu nome e/ou CPF/CNPJ.
        :param nome: o nome da pessoa ou instituição. Obrigatório se não for informado o CPF/CNPJ
        :param cpf_cnpj: o CPF/CNPJ da pessoa ou instituição. Obrigatório se não for informado o nome
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca

        >>> BuscaProcesso().por_envolvido(nome="Potelo Sistemas de Informacao",
        ...                               ordena_por=BuscaProcesso.Ordenacao.ULTIMA_MOVIMENTACAO,
        ...                               ordem=Ordem.ASC,
        ...                               tribunais=['TRF4']) # doctest: +SKIP

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

        return self.methods.get(f"envolvido/processos", data=data, params=params, **kwargs)

    def por_oab(self,
                numero: Union[str, int],
                estado: str,
                ordena_por: Optional[Ordenacao] = None,
                ordem: Optional[Ordem] = None,
                ) -> Dict:
        """
        Retorna os processos de um advogado a partir de número da OAB.
        :param numero: o número da OAB
        :param estado: o estado de origem da OAB
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente

        >>> BuscaProcesso().por_oab(1234, "AC") # doctest: +SKIP

        >>> BuscaProcesso().por_oab(numero="123456",
        ...                         estado="SP",
        ...                         ordena_por=BuscaProcesso.Ordenacao.ULTIMA_MOVIMENTACAO,
        ...                         ordem=Ordem.DESC) # doctest: +SKIP
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
