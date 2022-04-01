from escavador.resources.endpoint import Endpoint
from escavador.exceptions import InvalidParamsException


class MonitoramentoTribunal(Endpoint):

    def get_monitoramentos(self):
        """
        Retorna todos os monitoramentos de tribunal do usuário
        :return: json
        """

        return self.methods.get("monitoramentos-tribunal")

    def get_monitoramento(self, id_monitoramento):
        """
        Retorna um monitoramento do usuário, de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: json
        """

        return self.methods.get(f"monitoramentos-tribunal/{id_monitoramento}")

    def editar_monitoramento(self, id_monitoramento, **kwargs):
        """
        Edita a frequencia de um monitoramento, de acordo com seu ID
        :param id_monitoramento:  o ID do monitoramento
        :keyword arguments:
            **frequencia**(``string``) -- a frequencia na qual o processo será monitorado
        :return: json
        """
        data = {
            'frequencia': kwargs.get('frequencia')
        }
        return self.methods.put(f"monitoramentos-tribunal/{id_monitoramento}", data=data)

    def criar_monitoramento(self, tipo_monitoramento, valor, **kwargs):
        """
        Cria um monitoramento de tribunal
        :param tipo_monitoramento: o tipo de monitoramento, opções disponiveis: UNICO, NUMDOC ,NOME
        :param valor: o valor que será monitorado no tribunal
        :keyword arguments:
            **frequencia**(``string``) -- a frequencia na qual o processo será monitorado
            **tribunal**(``string``) -- o tribunal a ser pesquisado
        :return: json
        """

        available_types = ['UNICO', 'NUMDOC', 'NOME']

        if tipo_monitoramento not in available_types:
            raise InvalidParamsException("Tipo de monitoramento inválido")

        if tipo_monitoramento is not 'UNICO' and kwargs.get('tribunal') is None:
            raise InvalidParamsException("O tribunal é obrigatório para esse tipo de monitoramento")

        data = {
            'tipo': tipo_monitoramento,
            'valor': valor,
            'tribunal': kwargs.get('tribunal'),
            'frequencia': kwargs.get('frequencia')
        }

        return self.methods.post("monitoramento-tribunal", data=data)

    def remover_monitoramento(self, id_monitoramento):
        """
        Remove um monitoramento de acordo com seu ID
        :param id_monitoramento: o ID do monitoramento
        :return: json
        """

        return self.methods.delete(f"monitoramentos-tribunal/{id_monitoramento}")
