from escavador.resources.endpoint import Endpoint
from escavador.exceptions import InvalidParamsException
from typing import Optional
from escavador.resources.enums import TiposMonitoramentosTribunal


class MonitoramentoTribunal(Endpoint):

    def get_monitoramentos(self) -> dict:
        """
        Retorna todos os monitoramentos de tribunal do usuário
        :return: dict
        """

        return self.methods.get("monitoramentos-tribunal")

    def get_monitoramento(self, id_monitoramento: int) -> dict:
        """
        Retorna um monitoramento do usuário, de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: dict
        """

        return self.methods.get(f"monitoramentos-tribunal/{id_monitoramento}")

    def editar_monitoramento(self, id_monitoramento: int, *, frequencia: Optional[str] = None) -> dict:
        """
        Edita a frequencia de um monitoramento, de acordo com seu ID
        :param frequencia: a frequencia na qual o processo será monitorado
        :param id_monitoramento:  o ID do monitoramento
        :return: dict
        """
        data = {
            'frequencia': frequencia
        }
        return self.methods.put(f"monitoramentos-tribunal/{id_monitoramento}", data=data)

    def criar_monitoramento(self, tipo_monitoramento: TiposMonitoramentosTribunal, valor: str, *,
                            frequencia: Optional[str] = None, tribunal: Optional[str] = None) -> dict:
        """
        Cria um monitoramento de tribunal
        :param tribunal: o tribunal a ser pesquisado
        :param frequencia: a frequencia na qual o processo será monitorado
        :param tipo_monitoramento: o tipo de monitoramento, opções disponiveis: UNICO, NUMDOC ,NOME
        :param valor: o valor que será monitorado no tribunal
        :return: dict
        """

        available_types = ['UNICO', 'NUMDOC', 'NOME']

        if tipo_monitoramento.value not in available_types:
            raise InvalidParamsException("Tipo de monitoramento inválido")

        if tipo_monitoramento.value is not TiposMonitoramentosTribunal.UNICO and tribunal is None:
            raise InvalidParamsException("O tribunal é obrigatório para esse tipo de monitoramento")

        data = {
            'tipo': tipo_monitoramento.value,
            'valor': valor,
            'tribunal': tribunal,
            'frequencia': frequencia
        }

        return self.methods.post("monitoramento-tribunal", data=data)

    def remover_monitoramento(self, id_monitoramento: int) -> dict:
        """
        Remove um monitoramento de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: dict
        """

        return self.methods.delete(f"monitoramentos-tribunal/{id_monitoramento}")
