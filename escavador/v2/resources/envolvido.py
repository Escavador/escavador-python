from dataclasses import dataclass, field

from typing import Optional, List, Dict, Tuple, Union, TYPE_CHECKING, Type

from escavador.exceptions import FailedRequest
from escavador.resources.helpers.enums_v2 import CriterioOrdenacao, Ordem, SiglaTribunal
from escavador.resources.helpers.endpoint import DataEndpoint
from escavador.resources.helpers.consume_cursor import consumir_cursor, json_to_class

if TYPE_CHECKING:
    from escavador.v2 import Processo


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


@dataclass
class EnvolvidoEncontrado:
    """Representação do envolvido encontrado na busca por envolvido.

    :attr nome: nome do envolvido
    :attr tipo_pessoa: tipo de pessoa do envolvido (ex: "FISICA")
    :attr quantidade_processos: quantidade de processos onde o envolvido apareceu
    :attr last_valid_cursor: cursor válido para a próxima página de resultados
    """

    nome: str
    tipo_pessoa: str
    quantidade_processos: int
    last_valid_cursor: str = field(default="None", hash=False, compare=False)
    _classe_buscada: Type["DataEndpoint"] = field(default=None, hash=False, compare=False)

    @classmethod
    def from_json(cls, json_dict: Optional[Dict], last_cursor: str = "", classe_buscada: Type["DataEndpoint"] = None) -> Optional["EnvolvidoEncontrado"]:
        if json_dict is None:
            return None

        return cls(
            nome=json_dict["nome"],
            tipo_pessoa=json_dict["tipo_pessoa"],
            quantidade_processos=json_dict["quantidade_processos"],
            last_valid_cursor=last_cursor,
            _classe_buscada=classe_buscada,
        )

    def continuar_busca(self) -> Union[List["DataEndpoint"], FailedRequest]:
        """Retorna mais resultados para a busca que gerou o objeto atual.

        :return: lista contendo a próxima página de resultados, ou FailedRequest em caso de erro
        """
        if self.last_valid_cursor and self._classe_buscada:
            resposta = consumir_cursor(self.last_valid_cursor)

            if not resposta["sucesso"]:
                conteudo = resposta.get("resposta", {})
                return FailedRequest(status=resposta["http_status"], **conteudo)

            self.last_valid_cursor = resposta["resposta"].get("links", {}).get("next", "")
            return json_to_class(resposta, self._classe_buscada.from_json, add_cursor=True)

        return []


@dataclass
class Envolvido(DataEndpoint):
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
    :attr last_valid_cursor: último cursor válido para a próxima página de resultados
    """

    nome: Optional[str]
    tipo: Optional[str]
    tipo_normalizado: str
    tipo_pessoa: str
    quantidade_processos: int
    polo: str
    prefixo: Optional[str] = None
    sufixo: Optional[str] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    oabs: List[Oab] = field(default_factory=list)
    advogados: List["Envolvido"] = field(
        default_factory=list, hash=False, compare=False
    )
    last_valid_cursor: str = field(default="", hash=False, compare=False)

    @classmethod
    def from_json(
        cls, json_dict: Optional[Dict], ultimo_cursor: str = ""
    ) -> Optional["Envolvido"]:
        if json_dict is None:
            return None

        return cls(
            tipo_pessoa=json_dict["tipo_pessoa"],
            quantidade_processos=json_dict["quantidade_processos"],
            nome=json_dict["nome"],
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

    @classmethod
    def processos(
        cls,
        cpf_cnpj: Optional[str] = None,
        nome: Optional[str] = None,
        ordena_por: Optional[CriterioOrdenacao] = None,
        ordem: Optional[Ordem] = None,
        tribunais: Optional[List[SiglaTribunal]] = None,
        **kwargs
    ) -> Union[Tuple[Optional[EnvolvidoEncontrado], List["Processo"]], FailedRequest]:
        """Busca os processos envolvendo uma pessoa ou instituição a partir de seu nome e/ou CPF/CNPJ.

        :param cpf_cnpj: CPF ou CNPJ do envolvido
        :param nome: nome do envolvido
        :param ordena_por: critério de ordenação dos resultados
        :param ordem: ordem de ordenação dos resultados
        :param tribunais: lista de tribunais para filtrar os resultados
        :return tupla com os dados do envolvido encontrado e uma lista de processos,
        ou FailedRequest caso ocorra algum erro
        """
        from escavador.v2 import Processo

        return Processo.por_envolvido(
            cpf_cnpj=cpf_cnpj,
            nome=nome,
            ordena_por=ordena_por,
            ordem=ordem,
            tribunais=tribunais,
            **kwargs
        )
