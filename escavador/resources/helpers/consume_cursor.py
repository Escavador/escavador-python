"""Oferece métodos para consumir um cursor e obter os próximos resultados de uma requisição na API V2"""
import re
from typing import Dict, Callable, Any

from escavador.method import Method

_methods = Method(api_version=2)


def _consumir_cursor(cursor: str) -> Dict:
    """Consome um cursor para obter os próximos resultados de uma busca
    :param cursor: url do cursor a ser consumido
    :return: um dicionário com a resposta da requisição
    """
    endpoint_cursor = re.sub(r".*/api/v\d/", "", cursor)
    return _methods.get(endpoint_cursor)


def get_up_to(resposta: Dict, qtd: int, constructor: Callable) -> Any:
    """Obtém os próximos resultados de uma busca até atingir a quantidade desejada ou erro

    :param resposta: a resposta da primeira requisição
    :param qtd: a quantidade de resultados desejada
    :param constructor: método para construir um objeto da resposta a partir do json
    :return: uma resposta extendida com até `qtd` resultados
    """
    while 0 < len(resposta["resposta"].get("items", [])) < qtd:
        cursor = resposta["resposta"].get("links", {}).get("next")
        if not cursor:
            break

        next_response = _consumir_cursor(cursor)
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
        items = resposta["resposta"]["items"][:qtd]
        cursor = resposta["resposta"].get("links", {}).get("next", "")
        objetos = [constructor(item) for item in items]
        for objeto in objetos:
            objeto.last_valid_cursor = cursor
        return objetos

    return resposta
