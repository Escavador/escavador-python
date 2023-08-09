import unittest
from escavador.resources.helpers.consume_cursor import json_to_class, consumir_cursor
from escavador.v2 import Tribunal


class TestJsonToClass(unittest.TestCase):
    def test_json_to_class_instancia(self):
        constructor_1 = str
        json_resposta = {"resposta": {"items": [{"id": 1}, {"id": 2}, {"id": 3}]}}
        result = json_to_class(json_resposta, constructor_1)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        for item in result:
            self.assertIsInstance(item, str)

    def test_json_to_class_adiciona_cursor(self):
        json_resposta = {"resposta": {"items": [{"id": 1}, {"id": 2}, {"id": 3}], "links": {"next": "EXPECTED_CURSOR"}}}
        result = json_to_class(
            json_resposta, lambda x, ultimo_cursor: dict(x, **{"cursor": ultimo_cursor}), add_cursor=True
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        for item in result:
            self.assertIsInstance(item, dict)
            self.assertIn("cursor", item)
            self.assertEqual(item["cursor"], "EXPECTED_CURSOR")

    def test_json_to_class_instancia_tribunais(self):
        json_resposta = {
            "resposta": {
                "items": [
                    {"id": 1, "nome": "Supremo Tribunal Federal", "sigla": "STF", "categoria": None, "estados": []},
                    {
                        "id": 2,
                        "nome": "Tribunal Regional do Trabalho da 1ª Região",
                        "sigla": "TRT-1",
                        "categoria": None,
                        "estados": [{"nome": "Rio de Janeiro", "sigla": "RJ"}],
                    },
                    {
                        "id": 3,
                        "nome": "Tribunal Regional do Trabalho da 2ª Região",
                        "sigla": "TRT-2",
                        "categoria": None,
                        "estados": [{"nome": "São Paulo", "sigla": "SP"}],
                    },
                    {
                        "id": 4,
                        "nome": "Tribunal Regional do Trabalho da 3ª Região",
                        "sigla": "TRT-3",
                        "categoria": None,
                        "estados": [{"nome": "Minas Gerais", "sigla": "MG"}],
                    },
                ],
                "links": {"next": None},
            }
        }
        result = json_to_class(json_resposta, Tribunal.from_json)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)
        for item in result:
            self.assertIsInstance(item, Tribunal)


class TestConsumirCursor(unittest.TestCase):
    def test_makes_request(self):
        response = consumir_cursor("invalid_endpoint_url_that_will_404")
        self.assertIsInstance(response, dict)
        self.assertEqual(response["http_status"], 404)
        self.assertEqual(response["sucesso"], False)
        self.assertGreaterEqual(len(response), 0)

    def test_request_api(self):
        response = consumir_cursor("https://www.escavador.com/api/v2/tribunais")
        self.assertIsInstance(response, dict)
        self.assertGreaterEqual(len(response), 0)


if __name__ == "__main__":
    unittest.main()
