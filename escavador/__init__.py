import escavador.v1
import escavador.v2
from ratelimit import RateLimitException
from escavador.v1 import (
    Busca,
    BuscaAssincrona,
    Processo,
    Callback,
    DiarioOficial,
    Instituicao,
    Jurisprudencia,
    Legislacao,
    MonitoramentoDiario,
    MonitoramentoTribunal,
    Movimentacao,
    Pessoa,
    Processo,
    Saldo,
    Tribunal
)
from escavador.resources import *
__APIKEY__ = None


def config(api_key: str):
    """
     Configura a chave da API do escavador
    :param api_key: o token da API
    :return:
    """
    global __APIKEY__
    __APIKEY__ = api_key
