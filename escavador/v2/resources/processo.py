from functools import total_ordering
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Union, Tuple

from escavador.exceptions import FailedRequest
from escavador.resources.helpers.endpoint import DataEndpoint
from escavador.resources.helpers.enums_v2 import Ordem, CriterioOrdenacao, SiglaTribunal
from escavador.resources.helpers.consume_cursor import json_to_class, consumir_cursor
from escavador.v2.resources.movimentacao import Movimentacao
from escavador.v2.resources.tribunal import Tribunal
from escavador.v2.resources.envolvido import Envolvido, EnvolvidoEncontrado


@dataclass
class Processo(DataEndpoint):
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
    :attr last_valid_cursor: link do cursor caso queira mais resultados. Não é um atributo do processo.
    """

    numero_cnj: str
    quantidade_movimentacoes: int
    fontes_tribunais_estao_arquivadas: bool
    ano_inicio: int
    data_ultima_verificacao: str
    tempo_desde_ultima_verificacao: str
    data_ultima_movimentacao: str
    titulo_polo_ativo: Optional[str] = None
    titulo_polo_passivo: Optional[str] = None
    data_inicio: Optional[str] = None
    fontes: List["FonteProcesso"] = field(default_factory=list)
    last_valid_cursor: str = field(default="", repr=False, hash=False)

    @classmethod
    def from_json(
        cls, json_dict: Optional[Dict], ultimo_cursor: str = ""
    ) -> Optional["Processo"]:
        if json_dict is None:
            return None

        instance = cls(
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

        return Processo.from_json(
            resposta["resposta"], resposta.get("links", {}).get("next", "")
        )

    @staticmethod
    def movimentacoes(
        numero_cnj: str, **kwargs
    ) -> Union[List[Movimentacao], FailedRequest]:
        """
        Busca as movimentações de um processo pelo seu número único do CNJ.

        :param numero_cnj: o número único do CNJ do processo
        :return: uma lista de movimentacoes, ou FailedRequest caso ocorra algum erro

        >>> Processo.movimentacoes("0000000-00.0000.0.00.0000") # doctest: +SKIP
        """
        data = kwargs

        first_response = Processo.methods.get(
            f"processos/numero_cnj/{numero_cnj}/movimentacoes", data=data, **kwargs
        )

        if not first_response["sucesso"]:
            conteudo = first_response.get("resposta", {})
            return FailedRequest(status=first_response["http_status"], **conteudo)

        return json_to_class(
            first_response, constructor=Movimentacao.from_json, add_cursor=True
        )

    @staticmethod
    def por_nome(
        nome: str,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        tribunais: Optional[List[SiglaTribunal]] = None,
        **kwargs,
    ) -> Union[List["Processo"], FailedRequest]:
        """
        Busca os processos envolvendo uma pessoa ou empresa a partir do seu nome.

        :param nome: o nome da pessoa ou empresa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :return: uma lista de processos, ou FailedRequest caso ocorra algum erro

        >>> Processo.por_nome("Escavador Engenharia e Construcoes Ltda") # doctest: +SKIP

        >>> Processo.por_nome("Escavador Engenharia e Construcoes Ltda",
        ...                   ordena_por=CriterioOrdenacao.INICIO,
        ...                   ordem=Ordem.DESC,
        ...                   tribunais=[SiglaTribunal.CNJ, SiglaTribunal.TRT10]) # doctest: +SKIP
        """
        return Processo.por_envolvido(
            nome=nome,
            ordena_por=ordena_por,
            ordem=ordem,
            tribunais=tribunais,
            **kwargs,
        )

    @staticmethod
    def por_cpf(
        cpf: str,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        tribunais: Optional[List[SiglaTribunal]] = None,
        **kwargs,
    ) -> Union[List["Processo"], FailedRequest]:
        """
        Busca os processos envolvendo uma pessoa a partir de seu CPF.

        :param cpf: o CPF da pessoa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :return: uma lista de processos, ou FailedRequest caso ocorra algum erro

        >>> Processo.por_cpf("123.456.789-99") # doctest: +SKIP

        >>> Processo.por_cpf("12345678999",
        ...                  ordena_por=CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                  ordem=Ordem.ASC,
        ...                  tribunais=[SiglaTribunal.STF]) # doctest: +SKIP
        """
        return Processo.por_envolvido(
            cpf_cnpj=cpf,
            ordena_por=ordena_por,
            ordem=ordem,
            tribunais=tribunais,
            **kwargs,
        )

    @staticmethod
    def por_cnpj(
        cnpj: str,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        tribunais: Optional[List[SiglaTribunal]] = None,
        **kwargs,
    ) -> Union[List["Processo"], FailedRequest]:
        """
        Busca os processos envolvendo uma instituição a partir de seu CNPJ.

        :param cnpj: o CNPJ da instituição
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :return: uma lista de processos, ou FailedRequest caso ocorra algum erro

        >>> Processo.por_cnpj("07838351002160") # doctest: +SKIP

        >>> Processo.por_cnpj("07.838.351/0021.60",
        ...                        ordena_por=CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                        ordem=Ordem.ASC,
        ...                        tribunais=[SiglaTribunal.TJBA, SiglaTribunal.TRF1]) # doctest: +SKIP
        """
        return Processo.por_envolvido(
            cpf_cnpj=cnpj,
            ordena_por=ordena_por,
            ordem=ordem,
            tribunais=tribunais,
            **kwargs,
        )

    @staticmethod
    def por_envolvido(
        cpf_cnpj: Optional[str] = None,
        nome: Optional[str] = None,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        tribunais: Optional[List[SiglaTribunal]] = None,
        **kwargs,
    ) -> Union[Tuple[Optional[EnvolvidoEncontrado], List["Processo"]], FailedRequest]:
        """
        Busca os processos envolvendo uma pessoa ou instituição a partir de seu nome e/ou CPF/CNPJ.

        É possível filtrar

        :param nome: o nome da pessoa ou instituição. Obrigatório se não for informado o CPF/CNPJ
        :param cpf_cnpj: o CPF/CNPJ da pessoa ou instituição. Obrigatório se não for informado o nome
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :return: tupla com os dados do envolvido encontrado e uma lista de processos,
        ou FailedRequest caso ocorra algum erro

        >>> Processo.por_envolvido(cpf_cnpj="07.838.351/0021.60") # doctest: +SKIP

        >>> Processo.por_envolvido(nome='Escavador Engenharia e Construcoes Ltda',
        ...                             ordena_por=CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                             ordem=Ordem.ASC,
        ...                             tribunais=[SiglaTribunal.TJBA]) # doctest: +SKIP
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

        envolvido_encontrado = EnvolvidoEncontrado.from_json(
            first_response["resposta"].get("envolvido_encontrado"),
            last_cursor=first_response["resposta"].get("links", {}).get("next", ""),
            classe_buscada=Processo,
        )

        return envolvido_encontrado, json_to_class(
            first_response, Processo.from_json, add_cursor=True
        )

    @staticmethod
    def por_oab(
        numero: Union[str, int],
        estado: str,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        **kwargs,
    ) -> Union[List["Processo"], FailedRequest]:
        """
        Busca os processos de um advogado a partir de sua carteira da OAB.

        :param numero: o número da OAB
        :param estado: o estado de origem da OAB
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :return: uma lista de processos, ou FailedRequest caso ocorra algum erro

        >>> Processo.por_oab(1234, "AC") # doctest: +SKIP

        >>> Processo.por_oab(numero="12345",
        ...                  estado="SP",
        ...                  ordena_por=CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                  ordem=Ordem.DESC) # doctest: +SKIP
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

        return json_to_class(first_response, Processo.from_json, add_cursor=True)

    def continuar_busca(self) -> Union[List["Processo"], FailedRequest]:
        """Retorna mais resultados para a busca que gerou o processo atual.

        :return: lista de processos ou FailedRequest
        """
        if self.last_valid_cursor:
            resposta = consumir_cursor(self.last_valid_cursor)

            if not resposta["sucesso"]:
                conteudo = resposta.get("resposta", {})
                return FailedRequest(status=resposta["http_status"], **conteudo)

            return json_to_class(resposta, self.from_json, add_cursor=True)

        return []


@dataclass
class FonteProcesso:
    """Uma fonte da qual foram extraídas as informações de um processo.

    :attr id: id da fonte no sistema do Escavador
    :attr descricao: descrição resumida da fonte (ex: "TJSP - 2º grau")
    :attr nome: nome completo da fonte (ex: "Tribunal de Justiça de São Paulo")
    :attr sigla: sigla da fonte (ex: "DJES")
    :attr tipo: tipo da fonte (ex: "TRIBUNAL")
    :attr grau: grau da instância do processo nessa fonte - 1 para 1º grau, 2 para 2º grau, 3 para 3º grau.
    :attr grau_formatado: grau do processo por extenso (ex: "Primeiro Grau")
    :attr sistema: sistema de onde o processo foi extraído (ex: "ESAJ")
    :attr data_inicio: data de início da tramitação do processo nessa fonte
    :attr data_ultima_movimentacao: data da última movimentação registrada do processo nessa fonte
    :attr data_ultima_verificacao: data da última verificação feita no sistema de origem pelo Escavador
    :attr quantidade_movimentacoes: quantidade de movimentações do processo nessa fonte
    :attr fisico: indica se o processo é físico ou eletrônico
    :attr segredo_justica: indica se o processo está sob segredo de justiça
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
    tipo: str
    grau: int
    grau_formatado: str
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
    tribunal: Optional[Tribunal] = None
    capa: Optional["CapaProcessoTribunal"] = field(
        default=None, hash=False, compare=False
    )
    envolvidos: List[Envolvido] = field(default_factory=list, hash=False, compare=False)

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
            url=json_dict["url"],
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
    """Informações da capa de um processo em uma fonte, quando foi extraído de um tribunal.

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
        default_factory=list, hash=False, compare=False
    )

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["CapaProcessoTribunal"]:
        if json_dict is None:
            return None

        instance = cls(
            assunto_principal_normalizado=Assunto.from_json(
                json_dict["assunto_principal_normalizado"]
            ),
            classe=json_dict["classe"],
            assunto=json_dict["assunto"],
            area=json_dict["area"],
            orgao_julgador=json_dict["orgao_julgador"],
            data_distribuicao=json_dict["data_distribuicao"],
            data_arquivamento=json_dict["data_arquivamento"],
            valor_causa=ValorCausa.from_json(json_dict["valor_causa"]),
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
    :attr nome: descrição do assunto em específico
    :attr nome_com_pai: descrição do assunto e seu pai (mais genérico)
    :attr path_completo: path completo do assunto, desde a raiz menos específica até o assunto em específico
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
    :attr valor_formatado: valor da causa formatado
    """

    valor: float
    moeda: str
    valor_formatado: str

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["ValorCausa"]:
        if json_dict is None or json_dict.get("valor") is None:
            return None

        return cls(
            valor=float(json_dict["valor"]),
            moeda=json_dict["moeda"] or "R$",
            valor_formatado=json_dict["valor_formatado"]
            or cls._formatar_valor(json_dict["valor"], json_dict["moeda"]),
        )

    @staticmethod
    def _formatar_valor(valor: float, moeda: str) -> str:
        """Formata um valor monetário para o formato brasileiro."""
        inteiros, centavos = f"{valor:.2f}".split(".")
        return (
            f"{moeda} "
            + "".join(
                reversed(
                    [
                        f"{x}{'' if i % 3 and i else '.'}"
                        for i, x in enumerate(reversed(inteiros))
                    ]
                )
            ).strip(".")
            + f",{centavos}"
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

    :attr valor: texto da informação
    :attr tipo: tipo ou significado da informação
    """

    valor: str
    tipo: str

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["InformacaoComplementar"]:
        if json_dict is None or "valor" not in json_dict or "tipo" not in json_dict:
            return None

        return cls(valor=json_dict["valor"], tipo=json_dict["tipo"])
