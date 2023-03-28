import re
from escavador.exceptions import FailedRequest
from functools import total_ordering
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Union, Any, Callable
from escavador.method import Method
from escavador.resources.helpers.endpoint import Endpoint
from escavador.resources.helpers.enums_v2 import Ordem, CriterioOrdenacao, SiglaTribunal


@dataclass
class Processo(Endpoint):
    """
    Representa um processo retornado pela API do Escavador.

    Oferece métodos estáticos para buscar processos e suas movimentações.

    :attr id: id do processo no sistema do Escavador
    :attr numero_cnj: número único do CNJ do processo (ex: 0000000-00.0000.0.00.0000)
    :attr quantidade_movimentacoes: quantidade de movimentações registrada no processo
    :attr fontes_tribunais_estao_arquivadas: se True, todos os tribunais que são fontes desse processo já o arquivaram
    :attr titulo_polo_ativo: título do polo ativo (parte que move a ação)
    :attr titulo_polo_passivo: título do polo passivo (parte que responde à ação)
    :attr ano_inicio: ano em que o processo foi iniciado
    :attr data_inicio: data em que o processo foi iniciado
    :attr data_ultima_movimentacao: data da última movimentação registrada no processo
    :attr data_ultima_verificacao: data da última verificação do processo no sistema de origem
    :attr tempo_desde_ultima_verificacao: tempo desde a última verificação do processo no sistema de origem.
    :attr fontes: lista de fontes do processo
    :attr last_valid_cursor: link do cursor caso queira mais resultados. Não é um atributo do processo, e sim da API.
    """

    methods = Method(api_version=2)
    id: int
    numero_cnj: str
    quantidade_movimentacoes: int
    fontes_tribunais_estao_arquivadas: bool
    ano_inicio: int
    titulo_polo_ativo: Optional[str] = None
    titulo_polo_passivo: Optional[str] = None
    data_inicio: Optional[str] = None
    data_ultima_movimentacao: Optional[str] = None
    data_ultima_verificacao: Optional[str] = None
    tempo_desde_ultima_verificacao: Optional[str] = None
    last_valid_cursor: str = ""  # link do cursor caso queira mais resultados. Não faz parte do processo na API
    fontes: List["FonteProcesso"] = field(default_factory=list)

    @classmethod
    def from_json(
        cls, json_dict: Optional[Dict], ultimo_cursor: str = ""
    ) -> Optional["Processo"]:
        if json_dict is None:
            return None

        instance = cls(
            id=json_dict.get("id"),
            numero_cnj=json_dict.get("numero_cnj"),
            quantidade_movimentacoes=json_dict.get("quantidade_movimentacoes", 0),
            fontes_tribunais_estao_arquivadas=json_dict.get(
                "fontes_tribunais_estao_arquivadas"
            ),
            titulo_polo_ativo=json_dict.get("titulo_polo_ativo"),
            titulo_polo_passivo=json_dict.get("titulo_polo_passivo"),
            ano_inicio=json_dict.get("ano_inicio"),
            data_inicio=json_dict.get("data_inicio", None),
            data_ultima_movimentacao=json_dict.get("data_ultima_movimentacao", None),
            data_ultima_verificacao=json_dict.get("data_ultima_verificacao", None),
            tempo_desde_ultima_verificacao=json_dict.get(
                "tempo_desde_ultima_verificacao", None
            ),
            last_valid_cursor=ultimo_cursor,
        )
        instance.fontes += [
            FonteProcesso.from_json(fonte)
            for fonte in json_dict.get("fontes", [])
            if fonte
        ]

        return instance

    @staticmethod
    def por_numero(numero_cnj: str, **kwargs) -> Union["Processo", FailedRequest]:
        """
        Busca os dados de um processo pelo seu número único do CNJ.

        :param numero_cnj: o número único do CNJ do processo
        :return: o processo encontrado, ou uma exception caso não seja encontrado

        >>> Processo.por_numero("0000000-00.0000.0.00.0000") # doctest: +SKIP
        """

        resposta = Processo.methods.get(f"processos/numero_cnj/{numero_cnj}", **kwargs)

        if not resposta["sucesso"]:
            conteudo = resposta.get("resposta", {})
            return FailedRequest(status=resposta["http_status"], **conteudo)

        return Processo.from_json(resposta["resposta"])

    @staticmethod
    def movimentacoes(
        numero_cnj: str, qtd: int = 100, **kwargs
    ) -> Union[List["Movimentacao"], FailedRequest]:
        """
        Busca as movimentações de um processo pelo seu número único do CNJ.

        :param numero_cnj: o número único do CNJ do processo
        :param qtd: quantidade desejada de movimentações a ser retornada pela query
        :return: uma lista de movimentacoes com no máximo `qtd` resultados, ou FailedRequest caso ocorra algum erro

        >>> Processo.movimentacoes("0000000-00.0000.0.00.0000") # doctest: +SKIP

        >>> Processo.movimentacoes("0000000-00.0000.0.00.0000", qtd=10) # doctest: +SKIP
        """
        data = kwargs

        first_response = Processo.methods.get(
            f"processos/numero_cnj/{numero_cnj}/movimentacoes", data=data, **kwargs
        )

        if not first_response["sucesso"]:
            conteudo = first_response.get("resposta", {})
            return FailedRequest(status=first_response["http_status"], **conteudo)

        return _get_up_to(first_response, qtd, constructor=Movimentacao.from_json)

    @staticmethod
    def por_nome(
        nome: str,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        tribunais: Optional[List[SiglaTribunal]] = None,
        qtd: int = 100,
        **kwargs,
    ) -> Union[List["Processo"], FailedRequest]:
        """
        Busca os processos envolvendo uma pessoa ou empresa a partir do seu nome.

        :param nome: o nome da pessoa ou empresa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query
        :return: uma lista de processos com no máximo `qtd` resultados, ou FailedRequest caso ocorra algum erro

        >>> Processo.por_nome("Escavador Engenharia e Construcoes Ltda",
        ...                   ordena_por=CriterioOrdenacao.INICIO,
        ...                   ordem=Ordem.DESC,
        ...                   tribunais=[SiglaTribunal.CNJ, SiglaTribunal.TRT10],
        ...                   qtd=1) # doctest: +SKIP

        >>> Processo.por_nome("Escavador Engenharia e Construcoes Ltda") # doctest: +SKIP
        """
        return Processo.por_envolvido(
            nome=nome,
            ordena_por=ordena_por,
            ordem=ordem,
            tribunais=tribunais,
            qtd=qtd,
            **kwargs,
        )

    @staticmethod
    def por_cpf(
        cpf: str,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        tribunais: Optional[List[SiglaTribunal]] = None,
        qtd: int = 100,
        **kwargs,
    ) -> Union[List["Processo"], FailedRequest]:
        """
        Busca os processos envolvendo uma pessoa a partir de seu CPF.

        :param cpf: o CPF da pessoa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query
        :return: uma lista de processos com no máximo `qtd` resultados, ou FailedRequest caso ocorra algum erro

        >>> Processo.por_cpf("12345678999",
        ...                  ordena_por=CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                  ordem=Ordem.ASC,
        ...                  tribunais=[SiglaTribunal.STF],
        ...                  qtd=200) # doctest: +SKIP

        >>> Processo.por_cpf("123.456.789-99") # doctest: +SKIP
        """
        return Processo.por_envolvido(
            cpf_cnpj=cpf,
            ordena_por=ordena_por,
            ordem=ordem,
            tribunais=tribunais,
            qtd=qtd,
            **kwargs,
        )

    @staticmethod
    def por_cnpj(
        cnpj: str,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        tribunais: Optional[List[SiglaTribunal]] = None,
        qtd: int = 100,
        **kwargs,
    ) -> Union[List["Processo"], FailedRequest]:
        """
        Busca os processos envolvendo uma instituição a partir de seu CNPJ.

        :param cnpj: o CNPJ da instituição
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query
        :return: uma lista de processos com no máximo `qtd` resultados, ou FailedRequest caso ocorra algum erro

        >>> Processo.por_cnpj("07.838.351/0021.60",
        ...                        ordena_por=CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                        ordem=Ordem.ASC,
        ...                        tribunais=[SiglaTribunal.TJBA, SiglaTribunal.TRF1],
        ...                        qtd=1) # doctest: +SKIP

        >>> Processo.por_cnpj("07838351002160") # doctest: +SKIP
        """
        return Processo.por_envolvido(
            cpf_cnpj=cnpj,
            ordena_por=ordena_por,
            ordem=ordem,
            tribunais=tribunais,
            qtd=qtd,
            **kwargs,
        )

    @staticmethod
    def por_envolvido(
        cpf_cnpj: Optional[str] = None,
        nome: Optional[str] = None,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        tribunais: Optional[List[SiglaTribunal]] = None,
        qtd: int = 100,
        **kwargs,
    ) -> Union[List["Processo"], FailedRequest]:
        """
        Busca os processos envolvendo uma pessoa ou instituição a partir de seu nome e/ou CPF/CNPJ.

        Caso seja necessário múltiplos requests para obter a quantidade de processos desejada e algum
        erro ocorra em um request intermediário, a função retorna todos os processos obtidos até o
        momento com o o status code do erro ocorrido nesse último request.

        :param nome: o nome da pessoa ou instituição. Obrigatório se não for informado o CPF/CNPJ
        :param cpf_cnpj: o CPF/CNPJ da pessoa ou instituição. Obrigatório se não for informado o nome
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query
        :return: uma lista de processos com no máximo `qtd` resultados, ou FailedRequest caso ocorra algum erro

        >>> Processo.por_envolvido(nome='Escavador Engenharia e Construcoes Ltda',
        ...                             ordena_por=CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                             ordem=Ordem.ASC,
        ...                             tribunais=[SiglaTribunal.TJBA],
        ...                             qtd=1) # doctest: +SKIP

        >>> Processo.por_envolvido(cpf_cnpj="07.838.351/0021.60") # doctest: +SKIP
        """
        data = {
            "nome": nome,
            "cpf_cnpj": cpf_cnpj,
            "tribunais": tribunais,
        }

        params = {
            "ordena_por": ordena_por.value if ordena_por else None,
            "ordem": ordem.value if ordem else None,
        }

        first_response = Processo.methods.get(
            "envolvido/processos", data=data, params=params, **kwargs
        )

        if not first_response["sucesso"]:
            conteudo = first_response.get("resposta", {})
            return FailedRequest(status=first_response["http_status"], **conteudo)

        return _get_up_to(first_response, qtd, Processo.from_json)

    @staticmethod
    def por_oab(
        numero: Union[str, int],
        estado: str,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        qtd: int = 100,
        **kwargs,
    ) -> Union[List["Processo"], FailedRequest]:
        """
        Busca os processos de um advogado a partir de sua carteira da OAB.

        :param numero: o número da OAB
        :param estado: o estado de origem da OAB
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param qtd: quantidade desejada de processos a ser retornada pela query
        :return: uma lista de processos com no máximo `qtd` resultados, ou FailedRequest caso ocorra algum erro

        >>> Processo.por_oab(1234, "AC") # doctest: +SKIP

        >>> Processo.por_oab(numero="12345",
        ...                       estado="SP",
        ...                       ordena_por=CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                       ordem=Ordem.DESC,
        ...                       qtd=1) # doctest: +SKIP
        """
        data = {
            "oab_numero": f"{numero}",
            "oab_estado": estado,
        }
        params = {
            "ordena_por": ordena_por.value if ordena_por else None,
            "ordem": ordem.value if ordem else None,
        }

        first_response = Processo.methods.get(
            "advogado/processos", data=data, params=params, **kwargs
        )

        if not first_response["sucesso"]:
            conteudo = first_response.get("resposta", {})
            return FailedRequest(status=first_response["http_status"], **conteudo)

        return _get_up_to(first_response, qtd, Processo.from_json)


def _consumir_cursor(cursor: str) -> Dict:
    """Consome um cursor para obter os próximos resultados de uma busca
    :param cursor: url do cursor a ser consumido
    :return: um dicionário com a resposta da requisição
    """
    endpoint_cursor = re.sub(r".*/api/v\d/", "", cursor)
    return Processo.methods.get(endpoint_cursor)


def _get_up_to(resposta: Dict, qtd: int, constructor: Callable) -> Any:
    """Obtém os próximos resultados de uma busca até atingir a quantidade desejada ou erro
    :param resposta: a resposta da primeira requisição
    :param qtd: a quantidade de resultados desejada
    :return: uma resposta extendida com até `qtd` resultados, onde resposta['status'] é o status
    code do último request feito, e resposta['success'] é True se pelo menos um request
    foi bem sucedida, e False caso contrário.
    """
    while 0 < len(resposta["resposta"].get("items", [])) < qtd:
        cursor = resposta["resposta"].get("links", {}).get("next")
        if not cursor:
            break

        next_response = _consumir_cursor(cursor)
        next_items = next_response["resposta"].get("items")
        if not next_items:
            resposta["http_status"] = next_response["http_status"]
            break

        resposta["resposta"]["items"].extend(next_items)

        # replace cursor with next cursor
        resposta["resposta"]["links"]["next"] = (
            next_response["resposta"].get("links", {}).get("next")
        )

    if "items" in resposta["resposta"]:
        items = resposta["resposta"]["items"][:qtd]
        cursor = resposta["resposta"].get("links", {}).get("next", "")
        processos = [constructor(item) for item in items]
        for processo in processos:
            processo.last_valid_cursor = cursor
        return processos

    return resposta


@dataclass
class FonteProcesso:
    """Uma fonte da qual foram extraídas as informações de um processo.

    :attr id: id da fonte no sistema do Escavador
    :attr descricao: descrição resumida da fonte (ex: "TJSP - 2º grau")
    :attr nome: nome completo da fonte (ex: "Tribunal de Justiça de São Paulo")
    :attr sigla: sigla da fonte (ex: "DJES")
    :attr tipo: tipo da fonte (ex: "TRIBUNAL")
    :attr grau: grau da instância do processo nessa fonte - 1 para 1º grau, 2 para 2º grau, 3 para 3º grau.
    :attr grau_formatado: grau do processo por extenso (ex: "Primeiro grau")
    :attr sistema: sistema de onde o processo foi extraído (ex: "ESAJ")
    :attr data_inicio: data de início da tramitação do processo nessa fonte
    :attr data_ultima_movimentacao: data da última movimentação registrada do processo nessa fonte
    :attr data_ultima_verificacao: data da última verificação feita no sistema de origem pelo Escavador
    :attr fisico: indica se o processo é físico ou digital
    :attr segredo_justica: indica se o processo está sob segredo de justiça
    :attr quantidade_movimentacoes: quantidade de movimentações do processo nessa fonte
    :attr arquivado: indica se o processo está arquivado
    :attr url: url do processo na fonte
    :attr caderno: indica o caderno do diário oficial em que o processo foi publicado
    :attr tribunal: informações do tribunal de origem do processo
    :attr capa: informações da capa do processo
    :attr envolvidos: pessoas e instituições envolvidas no processo
    """

    id: int
    processo_fonte_id: int
    descricao: str
    nome: str
    sigla: str
    grau: int
    grau_formatado: str
    tipo: str
    data_inicio: str
    data_ultima_movimentacao: str
    fisico: bool
    sistema: str
    quantidade_movimentacoes: int
    segredo_justica: Optional[bool] = None
    arquivado: Optional[bool] = None
    url: Optional[str] = None
    caderno: Optional[str] = None
    data_ultima_verificacao: Optional[str] = None
    tribunal: Optional["Tribunal"] = None
    capa: Optional["CapaProcessoTribunal"] = field(
        default=None, hash=False, compare=False
    )
    envolvidos: List["Envolvido"] = field(
        default_factory=list, hash=False, compare=False
    )

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["FonteProcesso"]:
        if json_dict is None:
            return None

        instance = cls(
            id=json_dict["id"],
            processo_fonte_id=json_dict["processo_fonte_id"],
            descricao=json_dict["descricao"],
            nome=json_dict["nome"],
            sigla=json_dict["sigla"],
            grau=json_dict["grau"],
            grau_formatado=json_dict["grau_formatado"],
            tipo=json_dict["tipo"],
            data_inicio=json_dict["data_inicio"],
            data_ultima_movimentacao=json_dict["data_ultima_movimentacao"],
            fisico=json_dict["fisico"],
            sistema=json_dict["sistema"],
            quantidade_movimentacoes=json_dict["quantidade_movimentacoes"],
            segredo_justica=json_dict.get("segredo_justica"),
            arquivado=json_dict.get("arquivado"),
            url=json_dict.get("url"),
            caderno=json_dict.get("caderno"),
            data_ultima_verificacao=json_dict.get("data_ultima_verificacao"),
            tribunal=Tribunal.from_json(json_dict.get("tribunal", None)),
            capa=CapaProcessoTribunal.from_json(json_dict.get("capa", None)),
        )

        instance.envolvidos += [
            Envolvido.from_json(env) for env in json_dict.get("envolvidos") or [] if env
        ]

        return instance


@dataclass
class CapaProcessoTribunal:
    """Informações da capa de um processo de tribunal.

    :attr assunto_principal_normalizado: assunto principal do processo, normalizado como objeto Assunto
    :attr assuntos_normalizados: lista de assuntos do processo, normalizados como objeto Assunto
    :attr classe: classe do processo naquele momento (ex: "Procedimento Comum")
    :attr assunto: descrição resumida do assunto do processo
    :attr area: área do processo (ex: "Cível")
    :attr orgao_julgador: órgão julgador do processo naquela fonte
    :attr data_distribuicao: data em que o processo foi distribuído
    :attr data_arquivamento: data em que o processo foi arquivado, caso esteja arquivado
    :attr valor_causa: valor monetário da causa do processo
    :attr informacoes_complementares: conjunto de informações complementares
    """

    assunto_principal_normalizado: Optional["Assunto"] = None
    assuntos_normalizados: List["Assunto"] = field(
        default_factory=list, hash=False, compare=False
    )
    classe: Optional[str] = None
    assunto: Optional[str] = None
    area: Optional[str] = None
    orgao_julgador: Optional[str] = None
    data_distribuicao: Optional[str] = None
    data_arquivamento: Optional[str] = None
    valor_causa: Optional["ValorCausa"] = None
    informacoes_complementares: List["InformacaoComplementar"] = field(
        default_factory=list
    )

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["CapaProcessoTribunal"]:
        if json_dict is None:
            return None

        instance = cls(
            assunto_principal_normalizado=Assunto.from_json(
                json_dict.get("assunto_principal_normalizado", None)
            ),
            classe=json_dict.get("classe"),
            assunto=json_dict.get("assunto"),
            area=json_dict.get("area"),
            orgao_julgador=json_dict.get("orgao_julgador"),
            data_distribuicao=json_dict.get("data_distribuicao"),
            data_arquivamento=json_dict.get("data_arquivamento"),
            valor_causa=ValorCausa.from_json(json_dict.get("valor_causa", None)),
        )

        instance.assuntos_normalizados += [
            Assunto.from_json(assunto)
            for assunto in json_dict.get("assuntos_normalizados") or []
            if assunto
        ]
        instance.informacoes_complementares += [
            InformacaoComplementar.from_json(info)
            for info in json_dict.get("informacoes_complementares") or []
            if info
        ]

        return instance


@dataclass
class Assunto:
    """O assunto de um processo em formato normalizado.

    :attr id: id do assunto no sistema do Escavador
    :attr nome: nome do assunto
    :attr nome_com_pai: nome do assunto com o seu assunto "pai"
    :attr path_completo: path completo do assunto, desde a raiz até o assunto mais específico
    """

    id: int
    nome: str = field(hash=False, compare=False)
    nome_com_pai: str = field(hash=False, compare=False)
    path_completo: str

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["Assunto"]:
        if json_dict is None:
            return None

        return cls(
            id=json_dict["id"],
            nome=json_dict["nome"],
            nome_com_pai=json_dict["nome_com_pai"],
            path_completo=json_dict["path_completo"],
        )


@total_ordering
@dataclass
class ValorCausa:
    """Valor monetário da causa de um processo.

    :attr valor: montante do valor da causa
    :attr moeda: moeda em que o valor da causa está expresso
    """

    valor: float
    moeda: str
    valor_formatado: str

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["ValorCausa"]:
        if (
            json_dict is None
            or not json_dict.get("valor")
            or not json_dict.get("moeda")
            or not json_dict.get("valor_formatado")
        ):
            return None

        return cls(
            valor=float(json_dict["valor"]),
            moeda=json_dict["moeda"],
            valor_formatado=json_dict["valor_formatado"],
        )

    def __eq__(self, other):
        if isinstance(other, ValorCausa):
            return self.valor == other.valor and self.moeda == other.moeda
        return False

    def __lt__(self, other):
        return (
            self.valor < other.valor
            if isinstance(other, ValorCausa) and self.moeda == other.moeda
            else False
        )

    def __str__(self):
        return self.valor_formatado


@dataclass
class InformacaoComplementar:
    """Informações complementares de um processo.

    :attr valor: valor da informação complementar
    :attr tipo: tipo da informação complementar
    """

    valor: str
    tipo: str

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["InformacaoComplementar"]:
        if json_dict is None or "valor" not in json_dict or "tipo" not in json_dict:
            return None

        return cls(valor=json_dict["valor"], tipo=json_dict["tipo"])


@dataclass()
class Movimentacao:
    """Uma movimentação em um processo.

    :attr id: id da movimentação no sistema do Escavador
    :attr fonte: fonte de onde a movimentação foi extraída
    :attr tipo: tipo de movimentação
    :attr conteudo: conteúdo da movimentação
    :attr data: data em que ocorreu
    """

    id: int
    data: str
    tipo: Optional[str] = None
    conteudo: str = ""
    fonte: "FonteMovimentacao" = field(default=None, hash=False, compare=False)

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["Movimentacao"]:
        if json_dict is None:
            return None

        return cls(
            id=json_dict["id"],
            fonte=FonteMovimentacao.from_json(json_dict.get("fonte", None)),
            tipo=json_dict.get("tipo"),
            conteudo=json_dict.get("conteudo"),
            data=json_dict.get["data"],
        )


@dataclass
class FonteMovimentacao:
    """Fonte de onde uma movimentação foi extraída.

    :attr id: id da fonte no sistema do Escavador
    :attr nome: nome completo da fonte (ex: "Tribunal de Justiça de São Paulo")
    :attr sigla: sigla da fonte (ex: "DJES")
    :attr tipo: tipo da fonte (ex: "TRIBUNAL")
    :attr grau: grau da instância do processo nessa fonte - 1 para 1º grau, 2 para 2º grau, 3 para 3º grau.
    :attr grau_formatado: grau do processo por extenso (ex: "Primeiro grau")
    :attr caderno: caso a fonte seja um diário, o caderno em que a movimentação foi publicada
    :attr tribunal: informações do tribunal da fonte, caso a fonte seja um tribunal
    """

    id: int
    nome: Optional[str] = None
    tipo: Optional[str] = None
    sigla: Optional[str] = None
    grau: Optional[int] = None
    grau_formatado: str = ""
    caderno: Optional[str] = field(default=None, hash=False, compare=False)
    tribunal: Optional["Tribunal"] = field(default=None, hash=False, compare=False)

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["FonteMovimentacao"]:
        if json_dict is None:
            return None

        return cls(
            id=json_dict["fonte_id"],
            nome=json_dict.get("nome"),
            tipo=json_dict.get("tipo"),
            sigla=json_dict.get("sigla"),
            grau=json_dict.get("grau"),
            grau_formatado=json_dict.get("grau_formatado"),
            caderno=json_dict.get("caderno"),
            tribunal=Tribunal.from_json(json_dict.get("tribunal")),
        )


@dataclass
class Tribunal:
    """Informações de um tribunal.

    :attr id: id do tribunal no sistema do Escavador
    :attr nome: nome completo do tribunal
    :attr sigla: sigla do tribunal
    :attr categoria: categoria do tribunal
    :attr estados: lista de estados que o tribunal abrange
    """

    id: int
    nome: str
    sigla: str
    categoria: Optional[str] = None
    estados: List[str] = field(
        default_factory=list, hash=False, compare=False
    )  # Será adicionado à API depois

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["Tribunal"]:
        if json_dict is None:
            return None

        return cls(
            id=json_dict["id"],
            nome=json_dict["nome"],
            sigla=json_dict["sigla"],
            categoria=json_dict.get("categoria"),
            estados=json_dict.get("estados", []),
        )


@dataclass
class Envolvido:
    """Representação de um envolvido em um processo, seja ele um advogado, um polo, um juiz, ou um terceiro.

    :attr id: id do envolvido no sistema do Escavador
    :attr quantidade_processos: quantidade de processos onde o envolvido apareceu
    :attr tipo_pessoa: tipo de pessoa do envolvido (ex: "FISICA")
    :attr nome: nome do envolvido (ex: "João da Silva")
    :attr nome_normalizado: nome do envolvido depois da normalização (como foi buscado no banco de dados)
    :attr prefixo: prefixos do nome do envolvido (ex: "Dr.")
    :attr sufixo: sufixos do nome do envolvido (ex: "Jr.")
    :attr tipo: tipo do envolvido (ex: "Advogado")
    :attr tipo_normalizado: tipo do envolvido padronizado pelo Escavador
    :attr polo: polo do envolvido nesse processo (ex: "NENHUM" ou "ATIVO")
    :attr documento: documento do envolvido (ex: "123.456.789-00" ou "12.345.678/0001-90")
    :attr cpf: CPF do envolvido, caso o envolvido seja uma pessoa física
    :attr cnpj: CNPJ do envolvido, caso o envolvido seja uma pessoa jurídica
    :attr advogados: lista de advogados do envolvido nessse processo
    :attr oabs: lista de carteiras da OAB do envolvido, caso o envolvido seja um advogado
    """

    tipo: str
    tipo_normalizado: str
    tipo_pessoa: str
    quantidade_processos: int
    polo: str
    nome: Optional[str] = None
    nome_normalizado: Optional[str] = None
    prefixo: Optional[str] = None
    sufixo: Optional[str] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    oabs: List["Oab"] = field(default_factory=list)
    advogados: List["Envolvido"] = field(
        default_factory=list, hash=False, compare=False
    )

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["Envolvido"]:
        if json_dict is None:
            return None

        return cls(
            tipo_pessoa=json_dict["tipo_pessoa"],
            quantidade_processos=json_dict["quantidade_processos"],
            nome=json_dict.get("nome"),
            nome_normalizado=json_dict.get("nome_normalizado"),
            prefixo=json_dict.get("prefixo"),
            sufixo=json_dict.get("sufixo"),
            tipo=json_dict["tipo"],
            tipo_normalizado=json_dict["tipo_normalizado"],
            polo=json_dict["polo"],
            cpf=json_dict.get("cpf"),
            cnpj=json_dict.get("cnpj"),
            oabs=[Oab.from_json(o) for o in json_dict.get("oabs", []) if o],
            advogados=[
                Envolvido.from_json(a) for a in json_dict.get("advogados", []) if a
            ],
        )

    @property
    def documento(self) -> Optional[str]:
        return self.cpf or self.cnpj


@dataclass
class Oab:
    """Representação de uma carteira da OAB.

    :attr numero: número da carteira da OAB
    :attr uf: estado da carteira da OAB
    :attr tipo: tipo da carteira da OAB (ex: "ADVOGADO")
    """

    numero: int
    uf: str
    tipo: str

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["Oab"]:
        if json_dict is None:
            return None

        return cls(
            numero=json_dict["numero"],
            uf=json_dict["uf"],
            tipo=json_dict["tipo"],
        )
