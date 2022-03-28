from escavador.api import Api
import asyncio


class Method(object):

    def __init__(self):
        self.api = Api()

    def get(self, url, **kwargs):
        return asyncio.run(self.api.request('GET', url, data=kwargs.get('data')))

    def post(self, url, **kwargs):
        return asyncio.run(self.api.request('POST', url, data=kwargs.get('data')))

    def put(self, url, **kwargs):
        return asyncio.run(self.api.request('PUT', url, data=kwargs.get('data')))

    def delete(self, url, **kwargs):
        return asyncio.run(self.api.request('DELETE', url, data=kwargs.get('data')))
