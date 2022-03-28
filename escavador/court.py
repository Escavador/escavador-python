from escavador.method import Method


class Court(object):

    def __init__(self):
        self.methods = Method()

    def get_available_court_systems(self):
        """
        Return all avaiable court systems
        :return: json containing all the available court systems
        """
        return self.methods.get("/tribunal/origens");

    def get_court_details(self, court_acronym):
        """
        Return the details about the specified court system
        :param court_acronym: the acronym of the searched court system
        :return: json containing the details about the specified court system
        """
        return self.methods.get("/tribunal/origens/{}".format(court_acronym));