class CustomListTypeHint(type):
    def __getitem__(self, item):
        if isinstance(item, type):
            item = item.__name__
        return f"{self.__name__}[{item}]"


class ListaResultados(list, metaclass=CustomListTypeHint):
    def continuar_busca(self) -> "ListaResultados":
        """Retorna a próxima página de resultados, caso exista."""
        return self[-1].continuar_busca() if len(self) else ListaResultados()

    def mais_paginas(self, num_paginas: int = 1) -> int:
        """Extende a lista de resultados com mais resultados, caso existam.

        :param num_paginas: informa quantas páginas adicionais devem ser solicitadas.
        Se omitido, busca-se apenas a próxima página.
        :return: Número de páginas adicionais recebidas com sucesso.
        """
        return sum(int(self._mais_uma_pagina()) for _ in range(num_paginas))

    def _mais_uma_pagina(self) -> bool:
        """Extende a lista de resultados com a próxima página, caso exista.

        :return: True se recebeu uma nova página com sucesso, False caso contrário.
        """
        if not len(self):
            return False

        novos_resultados = self[-1].continuar_busca()

        if not novos_resultados:
            return False

        if len(novos_resultados) > 1 and isinstance(
            novos_resultados[1], ListaResultados
        ):
            novos_resultados = novos_resultados[1]

        self.extend(novos_resultados)

        return True
