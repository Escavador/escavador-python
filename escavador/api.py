import os
from typing import Dict, Union

import requests

import escavador
from escavador.exceptions import ApiKeyNotFoundException
from urllib import parse
from dotenv import load_dotenv
from importlib_metadata import version

load_dotenv()

SUPPORTED_VERSIONS = [1, 2]


class Api(object):

    def __init__(self, version):
        if version not in SUPPORTED_VERSIONS:
            raise ValueError("Versão da API inválida")

        self.base_url = f'https://api.escavador.com/api/v{version}/'

        self.api_key = escavador.__APIKEY__
        if self.api_key is None:
            try:
                self.api_key = os.environ['ESCAVADOR_API_KEY']
            except KeyError:
                raise ApiKeyNotFoundException("Nenhuma chave da API foi informada")

    def headers(self) -> Dict:
        """
        Retorna os headers padrões para a API

        :return: Dict de headers
        """
        return {
            'User-Agent': 'escavador-python/' + version('escavador'),
            'Authorization': 'Bearer ' + self.api_key,
            'X-Requested-With': 'XMLHttpRequest'
        }

    def request(self, method: str,
                url: str,
                data: Dict = None,
                params: Dict = None,
                **kwargs) -> Union[Dict, bytes]:
        """
        Executa um request HTML para a API

        :param method: método HTML
        :param url: slug do endpoint a ser chamado
        :param data: dados a serem enviados no formato json
        :param params: parâmetros a serem enviados na URL
        :return: Union[Dict, bytes]
        """
        url = parse.urljoin(self.base_url, url)
        if data is not None:
            data = {k: v for k, v in data.items() if v is not None}
        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}
        with requests.Session() as session:
            with session.request(method=method, url=url, headers=self.headers(), json=data, params=params) as resp:
                if resp.headers['Content-Type'] == 'application/pdf':
                    return resp.content
                else:
                    content = resp.json()
                    code = resp.status_code
                    success = False if code >= 400 else True
                    return {
                        "resposta": content,
                        "http_status": code,
                        "sucesso": success
                    }
