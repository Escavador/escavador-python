from typing import Optional

from escavador.method import Method


class Endpoint(object):

    def __init__(self, api_version: Optional[int] = None):
        if api_version:
            self.methods = Method(api_version)
