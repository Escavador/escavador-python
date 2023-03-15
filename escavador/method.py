from escavador.api import Api


class Method(object):

    def __init__(self, api_version):
        self.api = Api(version=api_version)

    def get(self, url, *, data=None, params=None, **kwargs):
        return self.api.request('GET', url, data=data, params=params, **kwargs)

    def post(self, url, *, data=None, params=None, **kwargs):
        return self.api.request('POST', url, data=data, params=params, **kwargs)

    def put(self, url, *, data=None, params=None, **kwargs):
        return self.api.request('PUT', url, data=data, params=params, **kwargs)

    def delete(self, url, *, data=None, params=None, **kwargs):
        return self.api.request('DELETE', url, data=data, params=params, **kwargs)
