from dataclasses import dataclass, field

from typing import Optional, List, Dict, Tuple, Union, TYPE_CHECKING, Type

from escavador.resources import ListaResultados
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
    :attr cpfs_com_esse_nome: quantidade de CPFs homônimos do envolvido
    :attr last_valid_cursor: cursor válido para a próxima página de resultados
    """

    nome: str
    tipo_pessoa: str
    quantidade_processos: int = field(hash=False, compare=False)
    cpfs_com_esse_nome: int = field(default=0, hash=False, compare=False)
    last_valid_cursor: Optional[str] = field(default="", hash=False, compare=False, repr=False)
    _classe_buscada: Type["DataEndpoint"] = field(
        default=None, hash=False, compare=False, repr=False
    )

    @classmethod
    def from_json(
        cls,
        json_dict: Optional[Dict],
        last_cursor: str = "",
        classe_buscada: Type["DataEndpoint"] = None,
    ) -> Optional["EnvolvidoEncontrado"]:
        if json_dict is None:
            return None

        tipo_pessoa = json_dict.get(
            "tipo_pessoa", "FISICA"
        )  # Se não houver tipo_pessoa, assume-se que é advogado, isto é, pessoa física.
        return cls(
            nome=json_dict["nome"],
            tipo_pessoa=tipo_pessoa,
            quantidade_processos=json_dict["quantidade_processos"],
            cpfs_com_esse_nome=json_dict.get(
                "cpfs_com_esse_nome", 1 if tipo_pessoa == "FISICA" else 0
            ),
            last_valid_cursor=last_cursor,
            _classe_buscada=classe_buscada,
        )

    def continuar_busca(self) -> Union[ListaResultados["DataEndpoint"], FailedRequest]:
        """Retorna mais resultados para a busca que gerou o objeto atual.

        :return: lista contendo a próxima página de resultados, ou FailedRequest em caso de erro
        """
        if self.last_valid_cursor and self._classe_buscada:
            resposta = consumir_cursor(self.last_valid_cursor)

            if not resposta["sucesso"]:
                conteudo = resposta.get("resposta", {})
                raise FailedRequest(status=resposta["http_status"], **conteudo)

            self.last_valid_cursor = resposta["resposta"].get("links", {}).get("next", "")
            return json_to_class(resposta, self._classe_buscada.from_json, add_cursor=True)

        return ListaResultados()

    def __eq__(self, other):
        if isinstance(other, Envolvido):
            # se só tem um CPF com esse nome, podemos dar como certo que é a mesma pessoa
            # se houver mais que um, não podemos ter certeza
            return (
                self.nome == other.nome
                and self.tipo_pessoa == other.tipo_pessoa
                and self.cpfs_com_esse_nome < 2
            )
        elif isinstance(other, EnvolvidoEncontrado):
            return (
                self.nome == other.nome
                and self.tipo_pessoa == other.tipo_pessoa
                # se um nome de envolvido foi obtido em uma data anterior (e, por exemplo, salvo como Pickle e depois
                # recuperado) e o outro foi obtido em uma busca nova, o valor de cpfs_com_esse_nome pode ser diferente.
                # Por isso, é necessário verificar que ambos sinalizam um cpf único com esse nome.
                and self.cpfs_com_esse_nome < 2
                and other.cpfs_com_esse_nome < 2
            ) or self is other
        elif isinstance(other, str):
            return self.nome == other
        return False


@dataclass
class Envolvido(DataEndpoint):
    """Representação de um envolvido em um processo, seja ele um advogado, um polo, um juiz, ou um terceiro.

    :attr id: id do envolvido no sistema do Escavador
    :attr quantidade_processos: quantidade de processos onde o envolvido apareceu
    :attr tipo_pessoa: tipo de pessoa do envolvido (ex: "FISICA")
    :attr nome: nome do envolvido (ex: "João da Silva")
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
    advogados: List["Envolvido"] = field(default_factory=list, hash=False, compare=False)
    last_valid_cursor: str = field(default="", hash=False, compare=False, repr=False)

    @classmethod
    def from_json(cls, json_dict: Optional[Dict], ultimo_cursor: str = "") -> Optional["Envolvido"]:
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
            advogados=[Envolvido.from_json(a) for a in json_dict.get("advogados", []) if a],
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
        **kwargs,
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
            **kwargs,
        )

    def __eq__(self, other):
        if isinstance(other, EnvolvidoEncontrado):
            return other == self

        if isinstance(other, Envolvido):
            return (
                self.nome == other.nome
                and self.tipo_pessoa == other.tipo_pessoa
                and self.cpf == other.cpf
                and self.cnpj == other.cnpj
                and self.oabs == other.oabs
            )

        if isinstance(other, str):
            return self.nome == other

        return False


@dataclass
class TipoEnvolvidoPesquisado:
    """Representação padronizada do tipo que o envolvido pesquisado assumiu na fonte específica

    :attr id: identificador único do tipo
    :attr tipo: tipo do envolvido como aparece na fonte
    :attr tipo_normalizado: tipo do envolvido padronizado pelo Escavador
    :attr polo: polo do envolvido nesse processo (ex: "ATIVO", "PASSIVO", "ADVOGADO")
    """

    id: int
    tipo: str
    tipo_normalizado: str
    polo: str

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["TipoEnvolvidoPesquisado"]:
        if json_dict is None:
            return None

        return cls(
            id=json_dict["id"],
            tipo=json_dict["tipo"],
            tipo_normalizado=json_dict["tipo_normalizado"],
            polo=json_dict["polo"],
        )
