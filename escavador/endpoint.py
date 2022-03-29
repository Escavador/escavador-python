from escavador.method import Method


class Endpoint(object):

    def __init__(self):
        self.methods = Method()
        self.states = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF',' ES', 'GO', 'MA', 'MS', 'MT', 'MG', 'PA', 'PB', 'PR',
                       'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']