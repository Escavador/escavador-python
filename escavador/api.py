import os
import requests

import escavador
from escavador.exceptions import ApiKeyNotFoundException
from urllib import parse
from dotenv import load_dotenv

load_dotenv()


class Api(object):

    def __init__(self):
        self.base_url = 'https://api.escavador.com/api/v1/'
        self.api_key = escavador.__APIKEY__
        if self.api_key is None:
            try:
                self.api_key = os.environ['ESCAVADOR_API_KEY']
            except KeyError:
                raise ApiKeyNotFoundException("Nenhuma chave da API foi informada")

    def headers(self):
        return {
            'Authorization': 'Bearer ' + self.api_key,
            'X-Requested-With': 'XMLHttpRequest'
        }

    def request(self, method, url, **kwargs):
        url = parse.urljoin(self.base_url, url)
        data = kwargs.get('data')
        if data is not None:
            data = {key: value for key, value in kwargs.get('data').items() if value is not None}
        with requests.Session() as session:
            with session.request(method=method, url=url, headers=self.headers(), json=data) as resp:
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