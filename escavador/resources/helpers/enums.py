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


class TiposMonitoramentosTribunal(Enum):
    UNICO = 'UNICO'
    NUMERO_DOCUMENTO = 'NUMDOC'
    NOME = 'NOME'


class TiposMonitoramentosDiario(Enum):
    PROCESSO = 'processo'
    TERMO = 'termo'


class FrequenciaMonitoramentoTribunal(Enum):
    DIARIA = 'DIARIA'
    SEMANAL = 'SEMANAL'


class StatusCallback(Enum):
    SUCESSO = "sucesso"
    EM_TENTATIVA = "em_tentativa"
    ERRO = "erro"
