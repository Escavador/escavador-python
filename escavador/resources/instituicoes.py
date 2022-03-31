from escavador.resources.endpoint import Endpoint


class Instituicao(Endpoint):

    def get_instituicao(self, id_instituicao):
        """
        Retorna uma instituição de acordo com seu ID
        :argument id_instituicao o ID da instituição
        :return json
        """

        return self.methods.get(f"instituicoes/{id_instituicao}")

    def get_processos_instituicao(self, id_instituicao, **kwargs):
        """
        Retorna os processos de uma instituição
        :argument id_instituicao: o ID da instituição
        :keyword Arguments:
            **limit*(``int``) -- limita a quantidade de registros retornados
            **page**(``ìnt``) -- número da página
        :return json
        """

        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }
        return self.methods.get(f"instituicoes/{id_instituicao}/processos", data=data)

    def get_institution_persons(self, id_instituicao, **kwargs):
        """
        Retorna as pessoas de uma instituição
        :argument id_instituicao: o ID da instituição
        :keyword Arguments:
            **limit*(``int``) -- limita a quantidade de registros retornados\n
            **page**(``ìnt``) -- número da página\n
        :return json
        """

        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }
        return self.methods.get(f"instituicoes/{id_instituicao}/pessoas", data=data)