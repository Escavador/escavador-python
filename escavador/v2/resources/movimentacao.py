from dataclasses import dataclass, field
from typing import Optional, Dict, Union, TYPE_CHECKING

from escavador.resources import ListaResultados
from escavador.exceptions import FailedRequest
from escavador.v2.resources.tribunal import Tribunal
from escavador.resources.helpers.consume_cursor import consumir_cursor, json_to_class
from escavador.resources.helpers.endpoint import DataEndpoint

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
    tribunal: Optional[Tribunal] = field(default=None, hash=False, compare=False)

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


@dataclass(frozen=True)
class ClassificacaoMovimentacao:
    """Classificação de uma movimentação.

    :attr nome: título da classificação
    :attr descricao: descrição detalhada do significado daquele tipo de movimentação
    :attr hierarquia: hierarquia que a classificação ocupa na árvore de classificações
        Ex: "Documentos Externos > Elementos De Prova > Parecer > Parecer (Outros)"
    """

    nome: str
    descricao: str
    hierarquia: str


@dataclass
class Movimentacao(DataEndpoint):
    """Uma movimentação em um processo.

    :attr id: id da movimentação no sistema do Escavador
    :attr fonte: fonte de onde a movimentação foi extraída
    :attr tipo: tipo de movimentação
    :attr tipo_publicacao: tipo da movimentação, quando especificado no diário oficial
    :attr classificacao_predita: classificação do tipo de movimentação estimada pelo Escavador
    :attr conteudo: conteúdo da movimentação
    :attr texto_categoria: quando a movimentação faz parte de um grupo no diário oficial,
                           é a parte do texto que se refere a todo o grupo
    :attr data: data em que ocorreu
    :attr last_valid_cursor: link do cursor caso queira mais resultados. Não é um atributo da movimentação
    """

    id: int
    data: str
    tipo: Optional[str] = None
    tipo_publicacao: Optional[str] = None
    classificacao_predita: ClassificacaoMovimentacao = field(
        default=None, hash=False, compare=False
    )
    conteudo: str = ""
    texto_categoria: Optional[str] = None
    fonte: FonteMovimentacao = field(default=None, hash=False, compare=False)
    last_valid_cursor: str = field(default="", repr=False, hash=False)

    @classmethod
    def from_json(
        cls, json_dict: Optional[Dict], ultimo_cursor: str = ""
    ) -> Optional["Movimentacao"]:
        if json_dict is None:
            return None

        return cls(
            id=json_dict["id"],
            fonte=FonteMovimentacao.from_json(json_dict.get("fonte", None)),
            tipo=json_dict.get("tipo"),
            tipo_publicacao=json_dict.get("tipo_publicacao"),
            classificacao_predita=ClassificacaoMovimentacao(
                nome=json_dict["classificacao_predita"].get("nome"),
                descricao=json_dict["classificacao_predita"].get("descricao"),
                hierarquia=json_dict["classificacao_predita"].get("hierarquia"),
            )
            if json_dict.get("classificacao_predita")
            else None,
            conteudo=json_dict.get("conteudo"),
            texto_categoria=json_dict.get("texto_categoria"),
            data=json_dict["data"],
            last_valid_cursor=ultimo_cursor,
        )

    @staticmethod
    def movimentacoes(
        processo: Union["Processo", str], **kwargs
    ) -> Union[ListaResultados["Movimentacao"], FailedRequest]:
        """Busca as movimentações de um processo.

        Alias do método `Processo.movimentacoes`.

        :param processo: número do processo ou instância de Processo
        :return: lista de movimentações ou FailedRequest

        >>> Processo.movimentacoes("0000000-00.0000.0.00.0000") # doctest: +SKIP
        """
        from escavador.v2 import Processo

        return (
            Processo.movimentacoes(processo.numero_cnj, **kwargs)
            if isinstance(processo, Processo)
            else Processo.movimentacoes(processo, **kwargs)
        )

    def continuar_busca(self) -> Union[ListaResultados["Movimentacao"], FailedRequest]:
        """Retorna mais resultados para a busca que gerou a movimentação atual.

        :return: lista de movimentações ou FailedRequest

        >>> Processo.movimentacoes("0000000-00.0000.0.00.0000") # doctest: +SKIP
        """
        if self.last_valid_cursor:
            resposta = consumir_cursor(self.last_valid_cursor)

            if not resposta["sucesso"]:
                conteudo = resposta.get("resposta", {})
                raise FailedRequest(status=resposta["http_status"], **conteudo)

            return json_to_class(resposta, self.from_json, add_cursor=True)

        return ListaResultados()
