from escavador.resources.helpers.endpoint import Endpoint
from typing import Optional, List, Dict
from escavador.resources.helpers.enums import TiposMonitoramentosDiario

class MonitoramentoDiario(Endpoint):

    def __init__(self):
        super().__init__(api_version=1)

    def origens(self, id_monitoramento: int) -> Dict:
        """
        Retorna os diários oficiais de um monitoramento
        :param id_monitoramento: o ID do monitoramento
        :return: Dict
        """

        return self.methods.get(f"monitoramentos/{id_monitoramento}/origens")

    def criar(self, tipo_monitoramento: TiposMonitoramentosDiario, *, termo: Optional[str] = None,
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

        return self.methods.post("monitoramentos", data=data)

    def monitoramentos(self) -> Dict:
        """
        Retorna todos os monitoramentos de diários oficiais do usuário
        :return: Dict
        """

        return self.methods.get("monitoramentos")

    def por_id(self, id_monitoramento: int) -> Dict:
        """
        Retorna um monitoramento de diários oficiais de acordo com seu ID
        :param id_monitoramento o ID do monitoramento
        :return: Dict
        """

        return self.methods.get(f"monitoramentos/{id_monitoramento}")

    def editar(self, id_monitoramento: int, *, variacoes: Optional[List[str]] = None,
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

        return self.methods.put(f"monitoramentos/{id_monitoramento}", data=data)

    def remover(self, id_monitoramento: int) -> Dict:
        """
        Remove um monitoramento de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: Dict
        """

        return self.methods.delete(f"monitoramentos/{id_monitoramento}")

    def aparicoes(self, id_monitoramento: int) -> Dict:
        """
        Retorna as aparições de um monitoramento pelo identificador do monitoramento.
        :param id_monitoramento: O ID do monitoramento
        :return: Dict
        """

        return self.methods.get(f"monitoramentos/{id_monitoramento}/aparicoes")

    def test_callback_monitoramento(self, callback_url: str, *, tipo: Optional[str] = None) -> Dict:
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
        return self.methods.post("monitoramentos/testcallback", data=data)