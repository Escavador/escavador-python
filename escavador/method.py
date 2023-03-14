from escavador.api import Api


class Method(object):

    def __init__(self, api_version):
        self.api = Api(version=api_version)

    def get(self, url, **kwargs):
        return self.api.request('GET', url, data=kwargs.get('data'))

    def post(self, url, **kwargs):
        return self.api.request('POST', url, data=kwargs.get('data'))

    def put(self, url, **kwargs):
        return self.api.request('PUT', url, data=kwargs.get('data'))

    def delete(self, url, **kwargs):
        return self.api.request('DELETE', url, data=kwargs.get('data'))
