from typing import Optional, Dict, Union

from escavador.api import Api


class Method(object):
    def __init__(self, api_version):
        self.api = Api(version=api_version)

    def get(
        self,
        url: str,
        *,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs
    ) -> Union[Dict, bytes]:
        """Envia um GET para o endpoint especificado em `url`

        Keyword arguments extras são adicionados ao corpo da requisição (json)

        :param url: slug do endpoint da API
        :param data: Dados a serem enviados no corpo da requisição (json)
        :param params: Dados a serem enviados na query string da requisição
        :return: Json da resposta da API (Dict), ou arquivo binário (bytes) em caso de download
        """
        return self.api.request("GET", url, data=data, params=params, **kwargs)

    def post(
        self,
        url: str,
        *,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs
    ) -> Union[Dict, bytes]:
        """Envia um POST para o endpoint especificado em `url`

        Keyword arguments extras são adicionados ao corpo da requisição (json)

        :param url: slug do endpoint da API
        :param data: Dados a serem enviados no corpo da requisição (json)
        :param params: Dados a serem enviados na query string da requisição
        :return: Json da resposta da API (Dict), ou arquivo binário (bytes) em caso de download
        """
        return self.api.request("POST", url, data=data, params=params, **kwargs)

    def put(
        self,
        url: str,
        *,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs
    ) -> Union[Dict, bytes]:
        """Envia um PUT para o endpoint especificado em `url`

        Keyword arguments extras são adicionados ao corpo da requisição (json)

        :param url: slug do endpoint da API
        :param data: Dados a serem enviados no corpo da requisição (json)
        :param params: Dados a serem enviados na query string da requisição
        :return: Json da resposta da API (Dict), ou arquivo binário (bytes) em caso de download
        """
        return self.api.request("PUT", url, data=data, params=params, **kwargs)

    def delete(
        self,
        url: str,
        *,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs
    ) -> Union[Dict, bytes]:
        """Envia um DELETE para o endpoint especificado em `url`

        Keyword arguments extras são adicionados ao corpo da requisição (json)

        :param url: slug do endpoint da API
        :param data: Dados a serem enviados no corpo da requisição (json)
        :param params: Dados a serem enviados na query string da requisição
        :return: Json da resposta da API (Dict), ou arquivo binário (bytes) em caso de download
        """
        return self.api.request("DELETE", url, data=data, params=params, **kwargs)
