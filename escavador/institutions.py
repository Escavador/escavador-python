from escavador.method import Method
from escavador.exceptions import InvalidParamsException


class Institutions(object):

    def __init__(self):
        self.methods = Method()

    def get_institution(self, institution_id):
        """
        Return an institution based on the institution ID \n
        :argument institution_id the ID of an Institution
        :return response decoded json containing the response
        """
        if not isinstance(institution_id, int):
            try:
                institution_id = int(institution_id)
            except:
                raise InvalidParamsException("Wrong params type given")

        return self.methods.get("/instituicoes/{}".format(institution_id))

    def get_institution_lawsuit(self, institution_id, **kwargs):
        """
        Return the process of an institution based on the institution ID \n
        :argument institution_id: the ID of an Institution
        :keyword Arguments:
            **limit*(``int``) -- Limit the number of returned records \n
            **page**(``ìnt``) -- page number \n
        :return response decoded json containing the response
        """
        if not isinstance(institution_id, int):
            try:
                institution_id = int(institution_id)
            except:
                raise InvalidParamsException("Wrong params type given")

        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }
        return self.methods.get("/instituicoes/{}/processos".format(institution_id),data=data)

    def get_institution_persons(self, institution_id, **kwargs):
        """
        Return the people of an institution based on the institution ID \n
        :argument institution_id: the ID of an Institution
        :keyword Arguments:
            **limit*(``int``) -- Limit the number of returned records \n
            **page**(``ìnt``) -- page number \n
        :return response decoded json containing the response
        """

        if not isinstance(institution_id, int):
            try:
                institution_id = int(institution_id)
            except:
                raise InvalidParamsException("Wrong params type given")

        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }
        return self.methods.get("/instituicoes/{}/pessoas".format(institution_id), data=data)