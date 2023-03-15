from enum import Enum

from escavador.resources.helpers.endpoint import Endpoint
from escavador.resources.helpers.enums import Ordem
from typing import Optional, Dict, List


class Processo(Endpoint):
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
        """
        data = kwargs

        return self.methods.get(f"processos/numero_cnj/{numero_cnj}", data=data)

    def movimentacoes(self, numero_cnj: str, **kwargs) -> Dict:
        """
        Retorna as movimentações de um processo pelo seu número único do CNJ.
        >>> Processo().movimentacoes("0000000-00.0000.0.00.0000")
        {}
        :param numero_cnj: o número único do CNJ do processo
        :return:
        """
        data = kwargs

        return self.methods.get(f"processos/numero_cnj/{numero_cnj}/movimentacoes", data=data)

    def por_nome(self,
                 nome: str,
                 ordena_por: Optional[Ordenacao] = None,
                 ordem: Optional[Ordem] = None,
                 tribunais: Optional[List] = None,
                 **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma pessoa ou empresa a partir do seu nome.
        :param nome: o nome da pessoa ou empresa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de números identificadores de tribunais para filtrar a busca
        """
        return self.por_envolvido(nome=nome, ordena_por=ordena_por, ordem=ordem, tribunais=tribunais, **kwargs)

    def por_cpf(self,
                cpf: str,
                ordena_por: Optional[Ordenacao] = None,
                ordem: Optional[Ordem] = None,
                tribunais: Optional[List] = None,
                **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma pessoa a partir de seu CPF.
        :param cpf: o CPF da pessoa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de números identificadores de tribunais para filtrar a busca
        """

    def por_cnpj(self,
                 cnpj: str,
                 ordena_por: Optional[Ordenacao] = None,
                 ordem: Optional[Ordem] = None,
                 tribunais: Optional[List] = None,
                 **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma instituição a partir de seu CNPJ.
        :param cnpj: o CNPJ da instituição
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de números identificadores de tribunais para filtrar a busca
        """
        return self.por_envolvido(cpf_cnpj=cnpj, ordena_por=ordena_por, ordem=ordem, tribunais=tribunais, **kwargs)

    def por_envolvido(self,
                      cpf_cnpj: Optional[str] = None,
                      nome: Optional[str] = None,
                      ordena_por: Optional[Ordenacao] = None,
                      ordem: Optional[Ordem] = None,
                      tribunais: Optional[List[int]] = None,
                      **kwargs) -> Dict:
        """
        Retorna os processos envolvendo uma pessoa ou instituição a partir de seu nome e/ou CPF/CNPJ.
        :param nome: o nome da pessoa ou instituição. Obrigatório se não for informado o CPF/CNPJ
        :param cpf_cnpj: o CPF/CNPJ da pessoa ou instituição. Obrigatório se não for informado o nome
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de números identificadores de tribunais para filtrar a busca
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
                oab: str,
                estado: str,
                ordena_por: Optional[Ordenacao] = None,
                ordem: Optional[Ordem] = None,
                ) -> Dict:
        """
        Retorna os processos de um advogado a partir de número da OAB.
        :param oab: o número da OAB
        :param estado: o estado de origem da OAB
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        """
        data = {
            'oab_numero': oab,
            'oab_estado': estado,
        }
        params = {
            'ordena_por': ordena_por.value if ordena_por else None,
            'ordem': ordem.value if ordem else None,
        }
        return self.methods.get(f"advogado/processos", data=data, params=params)
