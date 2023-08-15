import unittest
from escavador.v2 import Tribunal


class TestTribunal(unittest.TestCase):
    def test_montar_tribunal_from_json(self):
        json_dict = {
            "id": 81,
            "nome": "Tribunal Regional do Trabalho da 3ª Região",
            "sigla": "TRT-3",
            "categoria": None,
            "estados": [{"nome": "Minas Gerais", "sigla": "MG"}],
        }
        tribunal = Tribunal.from_json(json_dict)
        self.assertEqual(tribunal.id, 81)
        self.assertEqual(tribunal.nome, "Tribunal Regional do Trabalho da 3ª Região")
        self.assertEqual(tribunal.sigla, "TRT-3")
        self.assertEqual(tribunal.categoria, None)
        self.assertEqual(tribunal.estados[0].nome, "Minas Gerais")
        self.assertEqual(tribunal.estados[0].sigla, "MG")


if __name__ == "__main__":
    unittest.main()
