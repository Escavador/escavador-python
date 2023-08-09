import unittest
from escavador.resources.helpers.lista_resultados import ListaResultados
from escavador.v2 import Movimentacao


class TestListaResultados(unittest.TestCase):
    class MockDadoRetornado:
        def __init__(self):
            self.algum_dado = "algum dado"

        def continuar_busca(self):
            return [self.__class__() for _ in range(20)]

    def test_nao_eleva_exception_se_vazia(self):
        lista = ListaResultados()
        self.assertEqual(lista.continuar_busca(), ListaResultados())
        self.assertEqual(lista.mais_paginas(), 0)

    def test_retorna_vazio_se_nao_tem_mais_paginas(self):
        lista = ListaResultados()
        lista.append(
            Movimentacao(
                id=1,
                data="",
                last_valid_cursor="",  # É como é retornado na última página
            )
        )
        self.assertEqual(lista.continuar_busca(), ListaResultados())

    def test_continuar_busca(self):
        lista = ListaResultados([self.MockDadoRetornado() for i in range(20)])
        self.assertNotEqual(lista.continuar_busca(), lista)

    def test_mais_pagina(self):
        lista = ListaResultados([self.MockDadoRetornado() for i in range(20)])
        lista.mais_paginas()
        self.assertEqual(len(lista), 40)
        self.assertNotEqual(lista[:20], lista[20:])
        lista.mais_paginas()
        self.assertEqual(len(lista), 60)
        self.assertNotEqual(lista[:40], lista[40:])


if __name__ == "__main__":
    unittest.main()
