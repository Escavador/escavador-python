from escavador.method import Method


class Credits(object):

    def __init__(self):
        self.methods = Method()

    def get_credits(self):
        """
        Return the amount of credits of the user \n
        :return: json containing information about the user credits
        """
        return self.methods.get("/quantidade-creditos")
