from escavador.resources.helpers.endpoint import EndpointV1
from typing import Optional, Dict
from escavador.resources.helpers.enums_v1 import TiposMonitoramentosTribunal, FrequenciaMonitoramentoTribunal


class MonitoramentoTribunal(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def monitoramentos(cls) -> Dict:
        """
        Retorna todos os monitoramentos de tribunal do usuário
        :return: Dict
        """

        return cls.methods.get("monitoramentos-tribunal")

    @classmethod
    def por_id(cls, id_monitoramento: int) -> Dict:
        """
        Retorna um monitoramento do usuário, de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: Dict
        """

        return cls.methods.get(f"monitoramentos-tribunal/{id_monitoramento}")

    @classmethod
    def editar(cls, id_monitoramento: int, *, frequencia: Optional[str] = None) -> Dict:
        """
        Edita a frequencia de um monitoramento, de acordo com seu ID
        :param frequencia: a frequencia na qual o processo será monitorado
        :param id_monitoramento:  o ID do monitoramento
        :return: Dict
        """
        data = {
            'frequencia': frequencia
        }
        return cls.methods.put(f"monitoramentos-tribunal/{id_monitoramento}", data=data)

    @classmethod
    def criar(cls, tipo_monitoramento: TiposMonitoramentosTribunal, valor: str, *,
                            frequencia: Optional[FrequenciaMonitoramentoTribunal] = None,
                            tribunal: Optional[str] = None) -> Dict:
        """
        Cria um monitoramento de tribunal
        :param tribunal: o tribunal a ser pesquisado
        :param frequencia: a frequencia na qual o processo será monitorado
        :param tipo_monitoramento: o tipo de monitoramento, opções disponiveis: UNICO, NUMDOC ,NOME
        :param valor: o valor que será monitorado no tribunal
        :return: Dict
        """

        data = {
            'tipo': tipo_monitoramento.value,
            'valor': valor,
            'tribunal': tribunal,
            'frequencia': frequencia.value
        }

        return cls.methods.post("monitoramento-tribunal", data=data)

    @classmethod
    def remover(cls, id_monitoramento: int) -> Dict:
        """
        Remove um monitoramento de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: Dict
        """

        return cls.methods.delete(f"monitoramentos-tribunal/{id_monitoramento}")
