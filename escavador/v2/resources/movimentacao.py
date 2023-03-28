from dataclasses import dataclass, field
from typing import Optional, Dict, Union, List, TYPE_CHECKING

from escavador.exceptions import FailedRequest
from escavador.v2.resources.tribunal import Tribunal


if TYPE_CHECKING:
    from escavador.v2 import Processo


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
class Movimentacao:
    """Uma movimentação em um processo.

    :attr id: id da movimentação no sistema do Escavador
    :attr fonte: fonte de onde a movimentação foi extraída
    :attr tipo: tipo de movimentação
    :attr conteudo: conteúdo da movimentação
    :attr data: data em que ocorreu
    :attr last_valid_cursor: link do cursor caso queira mais resultados. Não é um atributo da movimentação.
    """

    id: int
    data: str
    tipo: Optional[str] = None
    conteudo: str = ""
    fonte: FonteMovimentacao = field(default=None, hash=False, compare=False)
    last_valid_cursor: str = field(default="", repr=False, hash=False)

    @classmethod
    def from_json(cls, json_dict: Optional[Dict]) -> Optional["Movimentacao"]:
        if json_dict is None:
            return None

        return cls(
            id=json_dict["id"],
            fonte=FonteMovimentacao.from_json(json_dict.get("fonte", None)),
            tipo=json_dict.get("tipo"),
            conteudo=json_dict.get("conteudo"),
            data=json_dict["data"],
        )

    @staticmethod
    def movimentacoes(
        processo: Union["Processo", str], qtd: int = 100, **kwargs
    ) -> Union[List["Movimentacao"], FailedRequest]:
        """Busca as movimentações de um processo.

        Alias do método `Processo.movimentacoes`.

        :param processo: número do processo ou instância de Processo
        :param qtd: quantidade desejada de processos a ser retornada
        """
        from escavador.v2.resources.processo import Processo

        return (
            Processo.movimentacoes(processo.numero_cnj, qtd=qtd)
            if isinstance(processo, Processo)
            else Processo.movimentacoes(processo, qtd=qtd)
        )