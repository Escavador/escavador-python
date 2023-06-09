from escavador.resources.helpers.endpoint import EndpointV1
from typing import Optional, List, Dict
from escavador.resources.helpers.enums_v1 import TiposMonitoramentosDiario


class MonitoramentoDiario(EndpointV1):

    def __init__(self):
        super().__init__()

    @classmethod
    def origens(cls, id_monitoramento: int) -> Dict:
        """
        Retorna os diários oficiais de um monitoramento
        :param id_monitoramento: o ID do monitoramento
        :return: Dict
        """

        return cls.methods.get(f"monitoramentos/{id_monitoramento}/origens")

    @classmethod
    def criar(cls, tipo_monitoramento: TiposMonitoramentosDiario, *, termo: Optional[str] = None,
                            origens_ids: Optional[List[int]] = None, processo_id: Optional[int] = None,
                            variacoes: Optional[List[str]] = None, termos_auxiliares: Optional[List[str]] = None
                            ) -> Dict:
        """
        Cria um novo monitoramento para termos ou processos
        :param termos_auxiliares: Array de array de strings com termos e condições
        :param variacoes: array de strings com as variações do termo monitorado.
        :param processo_id: o id do processo a ser monitorado nos diários.
        :param origens_ids: array de ids dos diarios que deseja monitorar
        :param termo: o termo a ser monitorado, obrigatório se tipo_monitoramento == termo
        :param tipo_monitoramento: o tipo de monitoramento: termo ou processo
        :return: Dict
        """

        data = {
            'tipo': tipo_monitoramento.value,
            'termo': termo,
            'origens_ids': origens_ids,
            'processo_id': processo_id,
            'variacoes': variacoes,
            'termos_auxiliares': termos_auxiliares
        }

        return cls.methods.post("monitoramentos", data=data)

    @classmethod
    def monitoramentos(cls) -> Dict:
        """
        Retorna todos os monitoramentos de diários oficiais do usuário
        :return: Dict
        """

        return cls.methods.get("monitoramentos")

    @classmethod
    def por_id(cls, id_monitoramento: int) -> Dict:
        """
        Retorna um monitoramento de diários oficiais de acordo com seu ID
        :param id_monitoramento o ID do monitoramento
        :return: Dict
        """

        return cls.methods.get(f"monitoramentos/{id_monitoramento}")

    @classmethod
    def editar(cls, id_monitoramento: int, *, variacoes: Optional[List[str]] = None,
                             origens_ids: Optional[List[str]] = None) -> Dict:
        """
        Edita os diários oficiais e as variações do termo do monitoramento
        :param id_monitoramento: o ID do monitoramento
        :param origens_ids: array de ids dos diarios que deseja monitorar
        :param variacoes: array de strings com as variações do termo monitorado.
        :return: Dict
        """
        data = {
            'variacoes': variacoes,
            'origens_ids': origens_ids
        }

        return cls.methods.put(f"monitoramentos/{id_monitoramento}", data=data)

    @classmethod
    def remover(cls, id_monitoramento: int) -> Dict:
        """
        Remove um monitoramento de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: Dict
        """

        return cls.methods.delete(f"monitoramentos/{id_monitoramento}")

    @classmethod
    def aparicoes(cls, id_monitoramento: int) -> Dict:
        """
        Retorna as aparições de um monitoramento pelo identificador do monitoramento.
        :param id_monitoramento: O ID do monitoramento
        :return: Dict
        """

        return cls.methods.get(f"monitoramentos/{id_monitoramento}/aparicoes")

    @classmethod
    def test_callback_monitoramento(cls, callback_url: str, *, tipo: Optional[str] = None) -> Dict:
        """
        Testa se a ulr de callback do usuário pode receber callbacks com resultados de monitoramentos
        :param callback_url: a url que o callback será enviado
        :param tipo o tipo de objeto do callback (movimentacao ou diario)
        :return: Dict
        """
        data = {
            'callback_url': callback_url,
            'tipo': tipo
        }
        return cls.methods.post("monitoramentos/testcallback", data=data)
