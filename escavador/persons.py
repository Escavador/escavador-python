from method import Method


class Persons(object):

    def __init__(self):
        self.methods = Method()

    def get_person(self,person_id):
        """
        Return an person based on the person ID \n
        :argument person_id the ID of an Person
        :return response decoded json containing the response
        """
        return self.methods.get("/pessoas/{}".format(person_id))

    def get_person_lawsuit(self,person_id, **kwargs):
        """
        Return the process of an person based on the person ID \n
        :argument person_id: the ID of an Person
        :keyword Arguments:
            **limit*(``int``) -- Limit the number of returned records \n
            **page**(``ìnt``) -- page number \n
        :return response decoded json containing the response
        """
        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }

        return self.methods.get("/pessoas/{}/processos".format(person_id), data=data)