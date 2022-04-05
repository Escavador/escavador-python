from escavador.resources import *

__APIKEY__ = None


def config(api_key):
    """
     Configura a chave da API do escavador
    :param api_key: o token da API
    :return:
    """
    global __APIKEY__
    __APIKEY__ = api_key
