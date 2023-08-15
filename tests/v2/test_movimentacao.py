import unittest
from escavador.v2 import Movimentacao


class TestMovimentacao(unittest.TestCase):
    def test_montar_movimentacao_from_json(self):
        json_dict_1 = {
            "id": 6572980630,
            "data": "2022-11-03",
            "tipo": "ANDAMENTO",
            "conteudo": "Juntada de petição intercorrente",
            "fonte": {
                "fonte_id": 15299,
                "nome": "Tribunal Regional Federal da 1ª Região",
                "tipo": "TRIBUNAL",
                "sigla": "TRF1",
                "grau": 1,
                "grau_formatado": "Primeiro Grau",
            },
        }
        movimentacao_1 = Movimentacao.from_json(json_dict_1, ultimo_cursor="EXPECTED_CURSOR")
        self.assertEqual(movimentacao_1.id, 6572980630)
        self.assertEqual(movimentacao_1.data, "2022-11-03")
        self.assertEqual(movimentacao_1.tipo, "ANDAMENTO")
        self.assertEqual(movimentacao_1.conteudo, "Juntada de petição intercorrente")
        self.assertEqual(movimentacao_1.fonte.id, 15299)
        self.assertEqual(movimentacao_1.fonte.nome, "Tribunal Regional Federal da 1ª Região")
        self.assertEqual(movimentacao_1.fonte.tipo, "TRIBUNAL")
        self.assertEqual(movimentacao_1.fonte.sigla, "TRF1")
        self.assertEqual(movimentacao_1.fonte.grau, 1)
        self.assertEqual(movimentacao_1.fonte.grau_formatado, "Primeiro Grau")
        self.assertEqual(movimentacao_1.last_valid_cursor, "EXPECTED_CURSOR")


if __name__ == "__main__":
    unittest.main()
