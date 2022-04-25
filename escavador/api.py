import os
import aiohttp
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

    async def request(self, method, url, **kwargs):
        url = parse.urljoin(self.base_url, url)
        data = kwargs.get('data')
        if data is not None:
            data = {key: value for key, value in kwargs.get('data').items() if value is not None}
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, headers=self.headers(), json=data) as resp:
                if resp.headers['Content-Type'] == 'application/pdf':
                    return await resp.read()
                else:
                    content = await resp.json()
                    code = resp.status
                    status = "Error" if code >= 400 else "Success"
                    return {
                        "content": content,
                        "code": code,
                        "status": status
                    }