from escavador.resources.helpers.endpoint import Endpoint
from typing import Optional
from escavador.resources.helpers.enums import TiposMonitoramentosTribunal, FrequenciaMonitoramentoTribunal


class MonitoramentoTribunal(Endpoint):

    def monitoramentos(self) -> dict:
        """
        Retorna todos os monitoramentos de tribunal do usuário
        :return: dict
        """

        return self.methods.get("monitoramentos-tribunal")

    def por_id(self, id_monitoramento: int) -> dict:
        """
        Retorna um monitoramento do usuário, de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: dict
        """

        return self.methods.get(f"monitoramentos-tribunal/{id_monitoramento}")

    def editar(self, id_monitoramento: int, *, frequencia: Optional[str] = None) -> dict:
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

    def criar(self, tipo_monitoramento: TiposMonitoramentosTribunal, valor: str, *,
                            frequencia: Optional[FrequenciaMonitoramentoTribunal] = None,
                            tribunal: Optional[str] = None) -> dict:
        """
        Cria um monitoramento de tribunal
        :param tribunal: o tribunal a ser pesquisado
        :param frequencia: a frequencia na qual o processo será monitorado
        :param tipo_monitoramento: o tipo de monitoramento, opções disponiveis: UNICO, NUMDOC ,NOME
        :param valor: o valor que será monitorado no tribunal
        :return: dict
        """

        data = {
            'tipo': tipo_monitoramento.value,
            'valor': valor,
            'tribunal': tribunal,
            'frequencia': frequencia.value
        }

        return self.methods.post("monitoramento-tribunal", data=data)

    def remover(self, id_monitoramento: int) -> dict:
        """
        Remove um monitoramento de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: dict
        """

        return self.methods.delete(f"monitoramentos-tribunal/{id_monitoramento}")
