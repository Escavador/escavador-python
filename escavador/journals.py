from escavador.method import Method


class Journals(object):

    def __init__(self):
        self.methods = Method()

    def get_sources(self):
        """
        Return all the sources from the official journals
        :return: json containing all the sources from de official journals
        """
        return self.methods.get("/origens")

    def get_page_from_journal(self, journal_id, **kwargs):
        """
        Return a specified page based on the journal informed
        :param journal_id: the ID of the searched journal
        :keyword arguments:
            **page**(``int``) -- the page from the informed journal
        :return: json containing the journal page information
        """
        data = kwargs.get('page')

        return self.methods.get("/diarios/{}".format(journal_id), data=data)

    def download_page_journal_pdf(self, journal_id, page):
        """
        Download a pdf of the page from the specified journal
        :param journal_id: ID from the journal source
        :param page: the page number
        :return: a pdf with the journal page
        """
        return self.methods.get("/diarios/{}/pdf/pagina/{}/baixar".format(journal_id, page))