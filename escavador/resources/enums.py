from enum import Enum


class TiposTermo(Enum):
    TODOS = "t"
    PESSOAS = "p"
    INSTITUICOES = "i"
    PATENTES = "pa"
    DIARIOS_OFICIAIS = "d"
    ENVOLVIDOS = "en"


class TiposBusca(Enum):
    BUSCA_POR_OAB = 'busca_por_oab'
    BUSCA_POR_DOCUMENTO = 'busca_por_documento'
    BUSCA_POR_NOME = 'busca_por_nome'


class TiposMonitoramentos(Enum):
    UNICO = 'UNICO'
    NUMERO_DOCUMENTO = 'NUMDOC'
    NOME = 'NOME'
