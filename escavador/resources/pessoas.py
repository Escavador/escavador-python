from escavador.resources.endpoint import Endpoint


class Pessoas(Endpoint):

    def get_pessoa(self, id_pessoa):
        """
        Retorna dados relacionados a uma pessoa pelo seu identificador.
        :param id_pessoa: o ID da pessoa
        :return: json
        """
        return self.methods.get(f"/pessoas/{id_pessoa}")

    def get_processos_pessoa(self,id_pessoa, **kwargs):
        """
        Return the process of an person based on the person ID \n
        :argument id_pessoa: o ID da pessoa
        :keyword Arguments:
            **limit*(``int``) -- limita a quantidade de registros retornados\n
            **page**(``ìnt``) -- número da página\n
        :return: json
        """
        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }

        return self.methods.get(f"/pessoas/{id_pessoa}/processos", data=data)