import escavador.v1
import escavador.v2

from ratelimit import RateLimitException
from escavador.exceptions import FailedRequest

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
from .api import config, __APIKEY__
