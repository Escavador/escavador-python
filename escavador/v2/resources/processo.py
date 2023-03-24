import re
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Union
from escavador.method import Method
from escavador.resources.helpers.endpoint import Endpoint
from escavador.resources.helpers.enums_v2 import Ordem, CriterioOrdenacao, SiglaTribunal


@dataclass
class Processo(Endpoint):
    """
    Oferece métodos para buscar processos e informações de processos no Escavador.

    Não é necessário instanciar esta classe, pois todos os métodos são estáticos.
    """
    methods = Method(api_version=2)
    numero_cnj: str
    titulo_polo_ativo: Optional[str]
    titulo_polo_passivo: Optional[str]
    ano_inicio: Optional[int]
    data_inicio: Optional[str]
    data_ultima_movimentacao: str  # TODO: acho que nao é optional, mas verificar
    quantidade_movimentacoes: int
    fontes_tribunais_estao_arquivadas: bool
    data_ultima_verificacao: str
    tempo_desde_ultima_verificacao: str
    last_valid_cursor: str  # link do cursor caso queira pegar mais resultados
    fontes: List["FonteProcesso"] = field(default_factory=list)

    @staticmethod
    def por_numero(numero_cnj: str, **kwargs) -> Dict:
        """
        Busca os dados de um processo pelo seu número único do CNJ.
        :param numero_cnj: o número único do CNJ do processo
        :return: dict com os campos ['resposta], ['status'] e ['success'].

        >>> Processo.por_numero("0000000-00.0000.0.00.0000") # doctest: +SKIP
        """

        return Processo.methods.get(
            f"processos/numero_cnj/{numero_cnj}", **kwargs
        )

    @staticmethod
    def movimentacoes(numero_cnj: str, qtd: int = 100, **kwargs) -> Dict:
        """
        Busca as movimentações de um processo pelo seu número único do CNJ.
        :param numero_cnj: o número único do CNJ do processo
        :param qtd: quantidade desejada de movimentações a ser retornada pela query
        :return: uma resposta com no máximo `qtd` resultados, onde resposta['status'] é o status
        code do último request feito, e resposta['success'] é True se pelo menos um request
        foi bem sucedida, e False caso contrário.

        >>> Processo.movimentacoes("0000000-00.0000.0.00.0000") # doctest: +SKIP

        >>> Processo.movimentacoes("0000000-00.0000.0.00.0000", qtd=10) # doctest: +SKIP
        """
        data = kwargs

        first_response = Processo.methods.get(
            f"processos/numero_cnj/{numero_cnj}/movimentacoes", data=data, **kwargs
        )
        return Processo._get_up_to(first_response, qtd)

    @staticmethod
    def por_nome(
            nome: str,
            ordena_por: Optional[CriterioOrdenacao] = None,
            ordem: Optional[Ordem] = None,
            tribunais: Optional[List[SiglaTribunal]] = None,
            qtd: int = 100,
            **kwargs,
    ) -> Dict:
        """
        Busca os processos envolvendo uma pessoa ou empresa a partir do seu nome.
        :param nome: o nome da pessoa ou empresa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query
        :return: uma resposta com no máximo `qtd` resultados, onde resposta['status'] é o status
        code do último request feito, e resposta['success'] é True se pelo menos um request
        foi bem sucedida, e False caso contrário.

        >>> Processo.por_nome("Escavador Engenharia e Construcoes Ltda",
        ...                        ordena_por=CriterioOrdenacao.INICIO,
        ...                        ordem=Ordem.DESC,
        ...                        tribunais=[SiglaTribunal.CNJ, SiglaTribunal.TRT10],
        ...                        qtd=1) # doctest: +SKIP

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
    ) -> Dict:
        """
        Busca os processos envolvendo uma pessoa a partir de seu CPF.
        :param cpf: o CPF da pessoa
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query
        :return: uma resposta com no máximo `qtd` resultados, onde resposta['status'] é o status
        code do último request feito, e resposta['success'] é True se pelo menos um request
        foi bem sucedida, e False caso contrário.

        >>> Processo.por_cpf("12345678999",
        ...                       ordena_por=CriterioOrdenacao.ULTIMA_MOVIMENTACAO,
        ...                       ordem=Ordem.ASC,
        ...                       tribunais=[SiglaTribunal.STF],
        ...                       qtd=200) # doctest: +SKIP

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
    ) -> Dict:
        """
        Busca os processos envolvendo uma instituição a partir de seu CNPJ.
        :param cnpj: o CNPJ da instituição
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param tribunais: lista de siglas de tribunais para filtrar a busca
        :param qtd: quantidade desejada de processos a ser retornada pela query
        :return: uma resposta com no máximo `qtd` resultados, onde resposta['status'] é o status
        code do último request feito, e resposta['success'] é True se pelo menos um request
        foi bem sucedida, e False caso contrário.

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
    ) -> Dict:
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
        :return: uma resposta com no máximo `qtd` resultados, onde resposta['status'] é o status
        code do último request feito, e resposta['success'] é True se pelo menos um request
        foi bem sucedida, e False caso contrário.

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

        return Processo._get_up_to(first_response, qtd)

    @staticmethod
    def por_oab(
            numero: Union[str, int],
            estado: str,
            ordena_por: Optional[CriterioOrdenacao] = None,
            ordem: Optional[Ordem] = None,
            qtd: int = 100,
            **kwargs,
    ) -> Dict:
        """
        Busca os processos de um advogado a partir de sua carteira da OAB.
        :param numero: o número da OAB
        :param estado: o estado de origem da OAB
        :param ordena_por: critério de ordenação
        :param ordem: determina ordenação ascendente ou descendente
        :param qtd: quantidade desejada de processos a ser retornada pela query
        :return: uma resposta com no máximo `qtd` resultados, onde resposta['status'] é o status
        code do último request feito, e resposta['success'] é True se pelo menos um request
        foi bem sucedida, e False caso contrário.

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

        return Processo._get_up_to(first_response, qtd)

    @staticmethod
    def _get_up_to(resposta: Dict, qtd: int) -> Dict:
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

            next_response = Processo._consumir_cursor(cursor)
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
            resposta["resposta"]["items"] = resposta["resposta"]["items"][:qtd]

        return resposta

    @staticmethod
    def _consumir_cursor(cursor: str) -> Dict:
        """Consome um cursor para obter os próximos resultados de uma busca
        :param cursor: url do cursor a ser consumido
        :return: um dicionário com a resposta da requisição
        """
        endpoint_cursor = re.sub(r".*/api/v\d/", "", cursor)
        return Processo.methods.get(endpoint_cursor)


@dataclass
class FonteProcesso:
    id: int
    processo_fonte_id: int
    descricao: str
    nome: str
    sigla: str
    grau: int
    grau_formatado: str
    tipo: str
    uf: str
    data_inicio: str
    data_ultima_movimentacao: str
    segredo_justica: Optional[bool]
    arquivado: Optional[bool]
    fisico: bool
    sistema: str
    capa: "CapaProcessoTribunal" = field(hash=False, compare=False)
    url: Optional[str]
    tribunal: Optional["Tribunal"]
    quantidade_movimentacoes: int
    caderno: Optional[str]
    data_ultima_verificacao: Optional[str]
    envolvidos: List["Envolvido"] = field(default_factory=list, hash=False, compare=False)


@dataclass
class CapaProcessoTribunal:
    classe: str
    assunto: str  # TODO: if None, get assunto_principal_normalizado.nome.upper()
    assuntos_normalizados: List["Assunto"]
    assunto_principal_normalizado: "Assunto"
    area: Optional[str]
    orgao_julgador: Optional[str]  # TODO: manter optional ou usar empty string?
    valor_causa: Optional["ValorCausa"] # Sempre vem na API, mas caso o conteudo seja null, seto como None aqui
    data_distribuicao: Optional[str]
    data_arquivamento: Optional[str]
    informacoes_complementares: List["InformacaoComplementar"] = field(default_factory=list)


@dataclass
class Assunto:
    id: int
    nome: str = field(hash=False, compare=False)
    nome_com_pai: str = field(hash=False, compare=False)
    path_completo: str = field(hash=False, compare=False)


@dataclass
class ValorCausa:
    valor: str
    moeda: str
    valor_formatado: Optional[str] = field(hash=False, compare=False) # R$ 0.000,00


class InformacaoComplementar:
    id: Optional[int]
    dado: Optional[str]
    processo: Optional["Processo"]
    created_at: Optional[str]
    updated_at: Optional[str]

    # Esses campos separados são dois formatos que vêm no JSON, às vezes vem o de cima, às vezes o de baixo
    # Era pra ser assim?

    valor: Optional[str]
    tipo: Optional[str]


@dataclass()
class Movimentacao:
    id: int
    data: str
    tipo: Optional[str]  # TODO: confirmar se realmente pode ser omitido/none
    conteudo: Optional[str]  # TODO: confirmar [segredo de justiça]
    fonte: "FonteMovimentacao"


@dataclass
class FonteMovimentacao:
    id: int
    nome: str
    sigla: str
    grau: int
    grau_formatado: str
    tipo: str
    caderno: Optional[str]
    tribunal: Optional["Tribunal"]


@dataclass
class Tribunal:
    id: int
    nome: str
    sigla: str
    categoria: str
    estados: List[str] = field(default_factory=list, hash=False, compare=False)
