from escavador.resources.helpers.endpoint import Endpoint
from typing import Optional, Dict


class Processo(Endpoint):

    def __init__(self):
        super().__init__(api_version=2)

    def por_numero(self, numero_cnj: str, ...) -> Dict:
        """
        Retorna os dados de um processo pelo seu número único do CNJ.
        :param numero_cnj: o número único do CNJ do processo
        :return: Dict
        """
        raise NotImplementedError

    def movimentacoes(self, numero_cnj: str, ...) -> Dict:
        """
        Retorna as movimentações de um processo pelo seu número único do CNJ.
        :param numero_cnj: o número único do CNJ do processo
        :return: Dict
        """
        raise NotImplementedError

    def processos_por_cpf(self, cpf: str, ...) -> Dict:
        """
        Retorna os processos de uma pessoa baseado no seu CPF.
        :param cpf: o CPF da pessoa
        :return: Dict
        """
        return self.__processos_por_documento(cpf, ...)

    def processos_por_cnpj(self, cnpj: str, ...) -> Dict:
        """
        Retorna os processos de uma instituição baseado no seu CNPJ.
        :param cnpj: o CNPJ da instituição
        :return: Dict
        """
        return self.__processos_por_documento(cnpj, ...)


    def __processos_por_documento(self, cpf_cnpj: str, ...) -> Dict:
        """
        Retorna os processos de uma pessoa ou instituição baseado no CPF/CNPJ.
        :param cpf_cnpj: o CPF/CNPJ da pessoa ou instituição
        :return: Dict
        """
        raise NotImplementedError

    def processos_por_oab(self, oab: str, ...) -> Dict:
        """
        Retorna os processos de um advogado baseado no número da OAB.
        :param oab: o número da OAB do advogado
        :return: Dict
        """
        raise NotImplementedError
