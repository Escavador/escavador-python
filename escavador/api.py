import os
import requests

from typing import Dict, Union
from importlib_metadata import version
from urllib import parse
from dotenv import load_dotenv
from ratelimit import limits

from escavador.exceptions import ApiKeyNotFoundException

load_dotenv()

SUPPORTED_VERSIONS = [1, 2]

DEFAULT_RATE_LIMIT = 500

__APIKEY__ = None


class Api(object):
    MAX_REQUESTS_PER_MIN = int(
        os.environ.get("ESCAVADOR_MAX_REQ_PER_MIN", DEFAULT_RATE_LIMIT)
    )

    def __init__(self, version):
        global __APIKEY__
        if version not in SUPPORTED_VERSIONS:
            raise ValueError("Versão da API inválida")

        self.base_url = f"https://api.escavador.com/api/v{version}/"

        if __APIKEY__ is None:
            try:
                __APIKEY__ = os.environ["ESCAVADOR_API_KEY"]
            except KeyError:
                pass

    @property
    def api_key(self) -> str:
        global __APIKEY__
        if __APIKEY__ is None:
            raise ApiKeyNotFoundException("Nenhuma chave da API foi informada")
        return __APIKEY__

    @api_key.setter
    def api_key(self, value: str):
        global __APIKEY__
        __APIKEY__ = value

    def headers(self) -> Dict:
        """
        Retorna os headers padrões para a API

        :return: Dict de headers
        """
        return {
            "User-Agent": "escavador-python/" + version("escavador"),
            "Authorization": f"Bearer {self.api_key}",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Encoding": "gzip, deflate, br",
        }

    @limits(calls=MAX_REQUESTS_PER_MIN, period=60)
    def request(
        self, method: str, url: str, data: Dict = None, params: Dict = None, **kwargs
    ) -> Union[Dict, bytes]:
        """
        Executa um request HTTP para a API

        Keyword arguments extras são adicionados ao corpo da requisição (json)

        :param method: método HTTP
        :param url: slug do endpoint a ser chamado
        :param data: dados a serem enviados no formato json
        :param params: parâmetros a serem enviados na URL
        :return: Union[Dict, bytes]
        """
        url = parse.urljoin(self.base_url, url)
        if data is not None:
            data = {k: v for k, v in data.items() if v is not None}
            data.update(
                {k: v for k, v in kwargs.items() if k not in data and v is not None}
            )
        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}
        with requests.Session() as session:
            with session.request(
                method=method, url=url, headers=self.headers(), json=data, params=params
            ) as resp:
                if resp.headers["Content-Type"] == "application/pdf":
                    return resp.content
                content = resp.json()
                code = resp.status_code
                success = code < 400
                return {"resposta": content, "http_status": code, "sucesso": success}


def config(api_key: str):
    """
     Configura a chave da API do escavador
    :param api_key: o token da API
    """
    global __APIKEY__
    __APIKEY__ = api_key
