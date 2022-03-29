from escavador.endpoint import Endpoint
from escavador.exceptions import InvalidParamsException


class SyncSearch(Endpoint):

    def search_word(self, word, word_type, **kwargs):
        """
        Search a word in the Escavador API
        :param word: the word to be searched
        :param word_type: the type of word to be searched (*t* - all types, *p* -- only persons,
         *i* -- only institutions, *pa* -- only patents, *d* -- only official journals,
          *en* -- only persons and institutions related to lawsuits)
        :keyword Arguments:
            **limit*(``int``) -- Limit the number of returned records \n
            **page**(``ìnt``) -- page number \n
        :return:json containing the result of the search
        """

        available_types = ['t', 'p', 'i', 'pa', 'd', 'en']

        if word_type not in available_types:
            raise InvalidParamsException("Invalid word type")

        data = {
            'q': word,
            'qo': word_type,
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }

        return self.methods.get("/busca", data=data)

    def get_lawsuit_by_oab(self, state, oab, **kwargs):
        """
        Search for lawsuit in the state journals with the oab number
        :param state: the state where te search will be performed
        :param oab: the oab number
        :keyword Arguments:
            **page**(``ìnt``) -- page number \n
        :return: json containing all the lawsuits found
        """

        data = {
            'page': kwargs.get('page')
        }

        if state not in self.states:
            raise InvalidParamsException("Invalid state")

        return self.methods.get("/oab/{}/{}/processos".format(state, oab), data=data)

    def get_lawsuit(self, lawsuit_id):
        """
        Return a lawsuit based on it's ID
        :param lawsuit_id: the lawsuit ID
        :return: json containing the lawsuit
        """

        return self.methods.get("/processos/{}".format(lawsuit_id))

    def get_lawsuit_motions(self, lawsuit_id, **kwargs):
        """
        Return all the motions for the sent lawsuit ID
        :param lawsuit_id: The lawsuit id
        :keyword Arguments:
            **limit*(``int``) -- Limit the number of returned records \n
            **page**(``ìnt``) -- page number \n
        :return: json containing all the motions
        """

        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }

        return self.methods.get("/processos/{}/movimentacoes".format(lawsuit_id), data=data)

    def get_lawsuit_by_unique_number(self, unique_number, **kwargs):
        """
        Return a lawsuit based on it's unique_number
        :param unique_number: the lawsuit unique number
        :keyword Arguments:
              **match_exato**(``boolean``) -- Return the lawsuit based on the full unique number sent 
        :return: json containing the found lawsuits
        """

        data = {
            'match_exato': kwargs.get('match_exato')
        }

        return self.methods.get("/processos/numero/{}".format(unique_number), data=data)

    def get_lawsuit_related_persons(self, lawsuit_id, **kwargs):
        """
        Return all the persons related to the lawsuit sent
        :param lawsuit_id: the lawsuit ID
        :keyword arguments:
            **limit*(``int``) -- Limit the number of returned records \n
            **page**(``ìnt``) -- page number \n
        :return: json containing all the persons related to de lawsuit
        """

        data = {
            'limit': kwargs.get('limit'),
            'page': kwargs.get('page')
        }

        return self.methods.get("/processos/{}/envolvidos".format(lawsuit_id), data=data)





