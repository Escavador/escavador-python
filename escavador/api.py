import aiohttp
import os
from dotenv import load_dotenv
import json
load_dotenv()


class Api(object):

    def __init__(self):
        self.base_url = os.environ['ESCAVADOR_BASE_URL']
        self.api_key = os.environ['ESCAVADOR_API_KEY']

    def headers(self):
        return {
            'Authorization': 'Bearer ' + self.api_key,
            'X-Requested-With': 'XMLHttpRequest'
        }

    async def request(self, method, url, **kwargs):
        url = self.base_url + url
        data = kwargs.get('data')
        if data is not None:
            data = {key: value for key, value in kwargs.get('data').items() if value is not None}
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method,url=url,headers=self.headers(), data=data) as response:
                return await response.json()