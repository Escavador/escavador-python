from dataclasses import dataclass, field
from typing import Optional, List, Dict


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

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["Envolvido"]:
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


@dataclass(frozen=True)
class EnvolvidoEncontrado:
    nome: str
    tipo_pessoa: str
    quantidade_processos: int

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["EnvolvidoEncontrado"]:
        if json_dict is None:
            return None

        return cls(
            nome=json_dict["nome"],
            tipo_pessoa=json_dict["tipo_pessoa"],
            quantidade_processos=json_dict["quantidade_processos"],
        )
