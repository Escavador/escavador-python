import unittest
from escavador.v2 import Processo
from v2 import Envolvido


class TestEnvolvido(unittest.TestCase):
    def test_montar_envolvido_from_json(self):
        json_dict_1 = {
            "nome": "Antonio Gomes Breitenfeld de Souza",
            "quantidade_processos": 20,
            "tipo_pessoa": "FISICA",
            "prefixo": None,
            "sufixo": None,
            "tipo": "RÉU/RÉ",
            "tipo_normalizado": "Réu",
            "polo": "PASSIVO",
            "cpf": "95812549170",
            "cnpj": None,
        }

        envolvido_1 = Envolvido.from_json(json_dict=json_dict_1)

        self.assertEqual(envolvido_1.nome, "Antonio Gomes Breitenfeld de Souza")
        self.assertEqual(envolvido_1.quantidade_processos, 20)
        self.assertEqual(envolvido_1.tipo_pessoa, "FISICA")
        self.assertEqual(envolvido_1.prefixo, None)
        self.assertEqual(envolvido_1.sufixo, None)
        self.assertEqual(envolvido_1.tipo, "RÉU/RÉ")
        self.assertEqual(envolvido_1.tipo_normalizado, "Réu")
        self.assertEqual(envolvido_1.polo, "PASSIVO")
        self.assertEqual(envolvido_1.cpf, "95812549170")
        self.assertEqual(envolvido_1.cnpj, None)

        json_dict_2 = {
            "nome": "Ministério Público Federal",
            "quantidade_processos": 3376681,
            "tipo_pessoa": "JURIDICA",
            "prefixo": None,
            "sufixo": None,
            "tipo": "AUTOR",
            "tipo_normalizado": "Autor",
            "polo": "ATIVO",
            "cpf": None,
            "cnpj": "03636198000192",
        }

        envolvido_2 = Envolvido.from_json(json_dict=json_dict_2)

        self.assertEqual(envolvido_2.nome, "Ministério Público Federal")
        self.assertEqual(envolvido_2.quantidade_processos, 3376681)
        self.assertEqual(envolvido_2.tipo_pessoa, "JURIDICA")
        self.assertEqual(envolvido_2.prefixo, None)
        self.assertEqual(envolvido_2.sufixo, None)
        self.assertEqual(envolvido_2.tipo, "AUTOR")
        self.assertEqual(envolvido_2.tipo_normalizado, "Autor")
        self.assertEqual(envolvido_2.polo, "ATIVO")
        self.assertEqual(envolvido_2.cpf, None)
        self.assertEqual(envolvido_2.cnpj, "03636198000192")

        json_dict_3 = {
            "nome": "Merlin de Escobar de Souza",
            "quantidade_processos": 45,
            "tipo_pessoa": "FISICA",
            "prefixo": None,
            "sufixo": None,
            "tipo": "Advogado",
            "tipo_normalizado": "Advogado",
            "polo": "ADVOGADO",
            "cpf": "06003114812",
            "cnpj": None,
            "oabs": [{"uf": "SP", "tipo": "ADVOGADO", "numero": 4482925}],
        }

        envolvido_3 = Envolvido.from_json(json_dict=json_dict_3)

        self.assertEqual(envolvido_3.nome, "Merlin de Escobar de Souza")
        self.assertEqual(envolvido_3.quantidade_processos, 45)
        self.assertEqual(envolvido_3.tipo_pessoa, "FISICA")
        self.assertEqual(envolvido_3.prefixo, None)
        self.assertEqual(envolvido_3.sufixo, None)
        self.assertEqual(envolvido_3.tipo, "Advogado")
        self.assertEqual(envolvido_3.tipo_normalizado, "Advogado")
        self.assertEqual(envolvido_3.polo, "ADVOGADO")
        self.assertEqual(envolvido_3.cpf, "06003114812")
        self.assertEqual(envolvido_3.cnpj, None)
        self.assertEqual(envolvido_3.oabs[0].uf, "SP")
        self.assertEqual(envolvido_3.oabs[0].tipo, "ADVOGADO")
        self.assertEqual(envolvido_3.oabs[0].numero, 4482925)


if __name__ == "__main__":
    unittest.main()
