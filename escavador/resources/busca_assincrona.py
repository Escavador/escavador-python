from escavador.resources.endpoint import Endpoint
from escavador.exceptions import InvalidParamsException
from escavador.validator import Validator


class BuscaAssincrona(Endpoint):

    def get_processo(self, numero_unico, **kwargs):
        """
        Cria uma busca assíncrona com o numero único, e busca por ele em todos os tribunais
        :param numero_unico: o numero único do processo
        :keyword arguments:
            **send_callback**(``boolean``) -- opção para mandar um callback com o resultado da busca
            **wait**(``boolean``) -- opção para esperar pelo resultado, espera no máximo 1 minuto
            **autos**(``boolean``) -- opção para retornar os autos do processo
            **usuario**(``string``) -- o usuário do advogado para o tribunal, obrigatório se autos == 1
            **senha**(``string``) -- a senha do advogado para o tribunal, obrigatório se autos == 1
            **origem**(``string``) -- sigla de um tribunal para fazer a busca, utilizado para forçar a busca em um
            tribunal diferente do tribunal do processo
        :return: json
        """

        data = {
            'send_callback': kwargs.get('send_callback'),
            'wait': kwargs.get('wait'),
            'autos': kwargs.get('autos'),
            'usuario': kwargs.get('usuario'),
            'senha': kwargs.get('senha'),
            'origem': kwargs.get('origem')
        }

        return self.methods.post(f"processo-tribunal/{numero_unico}/async", data=data)

    def get_processo_por_nome(self, origem, nome, **kwargs):
        """
        Cria uma busca assíncrona no tribunal de origem baseada no nome enviado
        :param origem: o tribunal onde a busca será realizada
        :param nome: o nome a ser buscado
        :keyword Arguments:
            **send_callback**(``boolean``) -- opção para mandar um callback com o resultado da busca
            **wait**(``boolean``) -- opção para esperar pelo resultado, espera no máximo 1 minuto
            **permitir_parcial**(``boolean``) -- opção para não fazer a busca em todos os sistemas de um tribunal
        :return: json
        """

        data = {
            'nome': nome,
            'permitir_parcial': kwargs.get('permitir_parcial'),
            'send_callback': kwargs.get('send_callback'),
            'wait': kwargs.get('wait')
        }

        return self.methods.post(f"tribunal/{origem.upper()}/busca-por-nome/async", data=data)

    def get_processo_por_documento(self, origem, numero_documento, **kwargs):
        """
        Cria uma busca assíncrona no tribunal de origem baseada no numero de documento enviado
        :param origem: o tribunal onde a busca será realizada
        :param numero_documento: o documento que será pesquisado
        :keyword Arguments:
            **send_callback**(``boolean``) -- opção para mandar um callback com o resultado da busca
            **wait**(``boolean``) -- opção para esperar pelo resultado, espera no máximo 1 minuto
            **permitir_parcial**(``boolean``) -- opção para não fazer a busca em todos os sistemas de um tribunal
        :return: json
        """

        data = {
            'numero_documento': numero_documento,
            'permitir_parcial': kwargs.get('permitir_parcial'),
            'send_callback': kwargs.get('send_callback'),
            'wait': kwargs.get('wait')
        }

        return self.methods.post(f"tribunal/{origem.upper()}/busca-por-documento/async", data=data)

    def get_processo_por_oab(self, origem, numero_oab, estado_oab, **kwargs):
        """
        Cria uma busca assíncrona no tribunal de origem baseada nos dados de oab enviados
        :param origem: o tribunal onde a busca será realizada
        :param numero_oab: o numero da oab que será pesquisado
        :param estado_oab: o estado da oab enviada
        :keyword Arguments:
           **send_callback**(``boolean``) -- opção para mandar um callback com o resultado da busca
            **wait**(``boolean``) -- opção para esperar pelo resultado, espera no máximo 1 minuto
            **permitir_parcial**(``boolean``) -- opção para não fazer a busca em todos os sistemas de um tribunal
        :return: json
        """

        data = {
            'numero_oab': numero_oab,
            'estado_oab': estado_oab,
            'permitir_parcial': kwargs.get('permitir_parcial'),
            'send_callback': kwargs.get('send_callback'),
            'wait': kwargs.get('wait')
        }

        return self.methods.post(f"tribunal/{origem.upper()}/busca-por-oab/async", data=data)

    def busca_em_lote(self, tipo_busca, origens, **kwargs):
        """
        Cria buscas do mesmo tipo para todos os tribunais enviados
        :param origens: os tribunais onde a busca será realizada
        :param tipo_busca: the tipe of search, available types: busca_por_nome, busca_por_documento, busca_por_oab
        :keyword Arguments:
            **send_callback**(``boolean``) -- opção para mandar um callback com o resultado da busca
            **numero_oab**(``string``) -- o numero da oab que será pesquisado
            **estado_oab**(``string``) -- o estado da oab enviada
            **numero_documento**(``string``) -- o documento que será pesquisado
            **name**(``string``) -- o nome que será pesquisado
        :return: json
        """

        available_types = ['busca_por_nome', 'busca_por_documento', 'busca_por_oab']

        origens = [origem.upper() for origem in origens]

        estado_oab = kwargs.get('estado_oab')

        if estado_oab is not None and estado_oab not in Validator.valid_states():
            raise InvalidParamsException("Estado inválido")

        if tipo_busca not in available_types:
            raise InvalidParamsException("Tipo de busca inválida")

        data = {
            'tipo': tipo_busca,
            'tribunais': origens,
            'nome': kwargs.get('nome'),
            'numero_documento': kwargs.get('numero_documento'),
            'numero_oab': kwargs.get('numero_oab'),
            'estado_oab': kwargs.get('estado_oab')
        }

        return self.methods.post("tribunal/async/lote", data=data)

    def get_todos_resultados(self):
        """
        Retorna todos os resultados de busca
        :return: json
        """

        return self.methods.get('async/resultados')

    def get_resultado(self, id_busca):
        """
        Retorna um resultado de busca específico
        :return: json
        """

        return self.methods.get(f'async/resultados/{id_busca}')

    def get_pdf(self, link_pdf, path, nome_arquivo):
        """
        Baixa um pdf de autos de acordo com seu link e salva no caminho enviado, com o nome enviado
        :param nome_arquivo: nome do arquivo a ser criado
        :param link_pdf: link do documento
        :param path: caminho onde o pdf será salvo
        :return: json
        """
        path = f"{path}/{nome_arquivo}.pdf"

        try:
            open(path, "x")

            conteudo = self.methods.get(link_pdf)

            arquivo = open(path, "+wb")
            arquivo.write(conteudo)
            arquivo.close()
        except FileExistsError as error:
            return {"error": error.strerror}
        except FileNotFoundError as error:
            return {"error": error.strerror}

        return {"path": path}
