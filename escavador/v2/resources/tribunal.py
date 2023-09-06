from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union

from escavador.exceptions import FailedRequest
from escavador.resources.helpers.consume_cursor import json_to_class
from escavador.resources.helpers.endpoint import DataEndpoint


@dataclass
class Tribunal(DataEndpoint):
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
    estados: List["Estado"] = field(default_factory=list, hash=False, compare=False)

    @classmethod
    def from_json(
        cls, json_dict: Optional[Dict], *, ultimo_cursor: Optional[str] = None
    ) -> Optional["Tribunal"]:
        if json_dict is None:
            return None

        return cls(
            id=json_dict["id"],
            nome=json_dict["nome"],
            sigla=json_dict["sigla"],
            categoria=json_dict.get("categoria"),
            estados=json_to_class(
                json_dict.get("estados", []),
                Estado.from_json,
                add_cursor=False,
            ),
        )

    @staticmethod
    def listar(estados: List[str] = None) -> Union[List["Tribunal"], FailedRequest]:
        """
        Lista os tribunais em que o Escavador possui crawlers e os estados que cada um abrange.

        No caso de tribunais de instância superior que abrangem todo o território nacional,
        a lista de estados será vazia.

        :param estados: permite que apenas tribunais que atendem os estados cujas siglas foram
        especificadas sejam retornados. Se não for especificado, todos os tribunais serão retornados.
        :return: lista de tribunais

        >>> Tribunal.listar() # doctest: +SKIP

        >>> Tribunal.listar(["SP", "RJ"]) # doctest: +SKIP
        """
        params = {}
        if estados is not None:
            params["estados[]"] = estados

        response = Tribunal.methods.get("tribunais", params=params)
        if not response["sucesso"]:
            conteudo = response.get("resposta", {})
            raise FailedRequest(status=response["http_status"], **conteudo)

        return json_to_class(response, Tribunal.from_json, add_cursor=False)


@dataclass
class Estado:
    """Informações de um ente federativo brasileiro.

    :attr nome: nome do estado
    :attr sigla: sigla do estado
    """

    nome: str
    sigla: str

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["Estado"]:
        if json_dict is None:
            return None

        return cls(nome=json_dict["nome"], sigla=json_dict["sigla"])
