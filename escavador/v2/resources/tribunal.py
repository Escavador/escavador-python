from dataclasses import dataclass, field
from typing import Optional, List, Dict


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
