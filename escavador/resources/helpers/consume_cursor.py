"""Oferece métodos para consumir um cursor e obter os próximos resultados de uma requisição na API V2"""
import re
from typing import Dict, Callable, List

from escavador.method import Method
from .lista_resultados import ListaResultados

_methods = Method(api_version=2)


def consumir_cursor(cursor: str) -> Dict:
    """Consome um cursor para obter os próximos resultados de uma busca

    :param cursor: url do cursor a ser consumido
    :return: a resposta da requisição
    """
    endpoint_cursor = re.sub(r".*/api/v\d/", "", cursor)
    return _methods.get(endpoint_cursor)


def json_to_class(
    resposta: Dict, constructor: Callable, add_cursor=False
) -> ListaResultados:
    """Instancia os itens de uma resposta a partir de um construtor

    :param resposta: a resposta da primeira requisição, onde 'items' é uma lista de dicts (jsons)
    :param constructor: método para construir um objeto da resposta a partir do json
    :param add_cursor: se True, adiciona o cursor da resposta ao objeto instanciado
    :return: uma lista de objetos instanciados
    """
    if isinstance(resposta, dict):
        resposta = resposta["resposta"]
        items, cursor_url = resposta["items"], resposta.get("links", {}).get("next", "")
    else:
        items, cursor_url = resposta, ""

    return ListaResultados(
        result
        for result in (
            [constructor(item, ultimo_cursor=cursor_url) for item in items]
            if add_cursor and cursor_url
            else [constructor(item) for item in items]
        )
        if result is not None
    )
