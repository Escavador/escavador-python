from escavador.resources.endpoint import Endpoint
from escavador.exceptions import InvalidParamsException


class MonitoramentoDiario(Endpoint):

    def get_diarios_monitoramento(self, id_monitoramento):
        """
        Retorna os diários oficiais de um monitoramento
        :param id_monitoramento: the monitor ID
        :return: json
        """

        return self.methods.get(f"monitoramentos/{id_monitoramento}/origens")

    def criar_monitoramento(self, tipo_monitoramento, **kwargs):
        """
        Cria um novo monitoramento para termos ou processos
        :param tipo_monitoramento: o tipo de monitoramento: termo ou processo
        :keyword arguments:
            **termo**(``string``) --o termo a ser monitorado, obrigatório se tipo_monitoramento == termo
            **origens_ids**(``int[]``) -- array de ids dos diarios que deseja monitorar
            **processo_id**(``string``) -- o id do processo a ser monitorado nos diários.
            **variacoes**(``string[]``) -- array de strings com as variações do termo monitorado.
            **termos_auxiliares**(``string[][]``) -- Array de array de strings com termos e condições
            para o alerta do monitoramento
        :return: json
        """

        if tipo_monitoramento not in ['termo', 'processo']:
            raise InvalidParamsException("Tipo de monitoramento inválido")

        data = {
            'tipo': tipo_monitoramento,
            'termo': kwargs.get('termo'),
            'origens_id': kwargs.get('origens_id'),
            'processo_id': kwargs.get('processo_id'),
            'variacoes': kwargs.get('variacoes'),
            'termos_auxiliares': kwargs.get('termos_auxiliares')
        }

        return self.methods.post("monitoramentos", data=data)

    def get_monitoramentos(self):
        """
        Retorna todos os monitoramentos de diários oficiais do usuário
        :return: json
        """

        return self.methods.get("monitoramentos")

    def get_monitoramento(self, id_monitoramento):
        """
        Retorna um monitoramento de diários oficiais de acordo com seu ID
        :param id_monitoramento o ID do monitoramento
        :return: json
        """

        return self.methods.get(f"monitoramentos/{id_monitoramento}")

    def editar_monitoramento(self, id_monitoramento, **kwargs):
        """
        Edita os diários oficiais e as variações do termo do monitoramento
        :param id_monitoramento: o ID do monitoramento
        :keyword arguments:
            **variacoes**(``string[]``) -- Array de array de strings com termos e condições
            **origens_ids**(``int[]``) -- array de ids dos diarios que deseja monitorar
        :return: json
        """
        data = {
            'variacoes': kwargs.get('variacoes'),
            'origens_ids': kwargs.get('origens_ids')
        }

        return self.methods.put(f"monitoramentos/{id_monitoramento}", data=data)

    def remover_monitoramento(self, id_monitoramento):
        """
        Remove um monitoramento de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: json
        """

        return self.methods.delete(f"monitoramentos/{id_monitoramento}")

    def get_aparicoes(self, id_monitoramento):
        """
        Retorna as aparições de um monitoramento pelo identificador do monitoramento.
        :param id_monitoramento: tho ID do monitoramento
        :return: json
        """

        return self.methods.get(f"monitoramentos/{id_monitoramento}/aparicoes")

    def test_callback_monitoramento(self, callback_url, **kwargs):
        """
        Testa se a ulr de callback do usuário pode receber callbacks com resultados de monitoramentos
        :param callback_url: a url que o callback será enviado
        :keyword arguments:
            **tipo**(``string``) -o tipo de objeto do callback: movimentacao ou diario
        :return: json
        """
        data = {
            'callback_url': callback_url,
            'tipo': kwargs.get('tipo')
        }
        return self.methods.post("monitoramentos/testcallback", data=data)
