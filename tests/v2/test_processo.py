import unittest
from escavador.v2 import Processo


class TestProcesso(unittest.TestCase):
    def test_montar_processo_from_json(self):
        json_dict = {
            "numero_cnj": "8690473-18.2023.4.01.4200",
            "titulo_polo_ativo": "Ministério Público Federal",
            "titulo_polo_passivo": "Nogueira Cavallero da Silva e outros",
            "ano_inicio": 2023,
            "data_inicio": "2023-04-01",
            "data_ultima_movimentacao": "2023-04-01",
            "quantidade_movimentacoes": 1,
            "fontes_tribunais_estao_arquivadas": False,
            "data_ultima_verificacao": "2023-04-01T13:45:30+00:00",
            "tipo_match": "NOME",
            "match_fontes": {
                "tribunal": True,
                "diario_oficial": False,
            },
            "tempo_desde_ultima_verificacao": "há 29 minutos",
            "fontes": [
                {
                    "id": 15399,
                    "processo_fonte_id": 222514338,
                    "descricao": "TRF1 - 1º grau",
                    "nome": "Tribunal Regional Federal da 1ª Região",
                    "sigla": "TRF1",
                    "tipo": "TRIBUNAL",
                    "data_inicio": "2023-04-01",
                    "data_ultima_movimentacao": "2023-04-01",
                    "segredo_justica": None,
                    "arquivado": None,
                    "status_predito": "ATIVO",
                    "grau": 1,
                    "grau_formatado": "Primeiro Grau",
                    "fisico": False,
                    "sistema": "PJE",
                    "capa": {
                        "classe": "AUTO DE PRISAO EM FLAGRANTE",
                        "assunto": "CRIMES CONTRA A ORDEM ECONOMICA",
                        "assuntos_normalizados": [
                            {
                                "id": 2027,
                                "nome": "Crimes contra a Ordem Econômica",
                                "nome_com_pai": (
                                    "Crimes Previstos na Legislação Extravagante > Crimes contra a Ordem Econômica"
                                ),
                                "path_completo": (
                                    "DIREITO PENAL > Crimes Previstos na Legislação Extravagante > Crimes contra a"
                                    " Ordem Econômica"
                                ),
                                "bloqueado": False,
                            },
                            {
                                "id": 2044,
                                "nome": "Crimes do Sistema Nacional de Armas",
                                "nome_com_pai": (
                                    "Crimes Previstos na Legislação Extravagante > Crimes do Sistema Nacional de Armas"
                                ),
                                "path_completo": (
                                    "DIREITO PENAL > Crimes Previstos na Legislação Extravagante > Crimes do Sistema"
                                    " Nacional de Armas"
                                ),
                                "bloqueado": False,
                            },
                        ],
                        "assunto_principal_normalizado": {
                            "id": 2027,
                            "nome": "Crimes contra a Ordem Econômica",
                            "nome_com_pai": (
                                "Crimes Previstos na Legislação Extravagante > Crimes contra a Ordem Econômica"
                            ),
                            "path_completo": (
                                "DIREITO PENAL > Crimes Previstos na Legislação Extravagante > Crimes contra a Ordem"
                                " Econômica"
                            ),
                            "bloqueado": False,
                        },
                        "area": None,
                        "orgao_julgador": "4ª VARA FEDERAL CRIMINAL DA SJRR",
                        "valor_causa": {
                            "valor": None,
                            "moeda": None,
                            "valor_formatado": None,
                        },
                        "data_distribuicao": "2023-04-01",
                        "data_arquivamento": None,
                        "informacoes_complementares": None,
                    },
                    "url": "https://pje1g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam",
                    "tribunal": {
                        "id": 5,
                        "nome": "Tribunal Regional Federal da 1ª Região",
                        "sigla": "TRF1",
                        "categoria": None,
                    },
                    "quantidade_movimentacoes": 1,
                    "quantidade_envolvidos": 1,
                    "match_documento_por": "DOCUMENTO_TRIBUNAL",
                    "data_ultima_verificacao": "2023-04-01T13:45:30+00:00",
                    "tipos_envolvido_pesquisado": [
                        {
                            "id": 3185,
                            "tipo": "Autoridade",
                            "tipo_normalizado": "Autoridade",
                            "polo": "ATIVO"
                        },
                        {
                            "id": 346,
                            "tipo": "autor do Fato",
                            "tipo_normalizado": "Réu",
                            "polo": "PASSIVO"
                        }
                    ],
                    "envolvidos": [
                        {
                            "nome": "Superintencia de Policia Federal Em Roraima",
                            "quantidade_processos": None,
                            "tipo_pessoa": "JURIDICA",
                            "prefixo": None,
                            "sufixo": None,
                            "tipo": "Autoridade",
                            "tipo_normalizado": "Autoridade",
                            "polo": "DESCONHECIDO",
                            "cnpj": "00394494009354",
                        }
                    ],
                }
            ],
        }
        processo = Processo.from_json(
            json_dict,
            ultimo_cursor="EXPECTED_CURSOR",
        )
        self.assertIsInstance(processo, Processo)
        self.assertEqual(processo.last_valid_cursor, "EXPECTED_CURSOR")
        self.assertEqual(processo.numero_cnj, "8690473-18.2023.4.01.4200")
        self.assertEqual(processo.titulo_polo_ativo, "Ministério Público Federal")
        self.assertEqual(processo.titulo_polo_passivo, "Nogueira Cavallero da Silva e outros")
        self.assertEqual(processo.ano_inicio, 2023)
        self.assertEqual(processo.data_inicio, "2023-04-01")
        self.assertEqual(processo.data_ultima_movimentacao, "2023-04-01")
        self.assertEqual(processo.quantidade_movimentacoes, 1)
        self.assertEqual(processo.data_ultima_verificacao, "2023-04-01T13:45:30+00:00")
        self.assertEqual(processo.tempo_desde_ultima_verificacao, "há 29 minutos")
        self.assertEqual(processo.tipo_match, "NOME")
        self.assertEqual(processo.fontes_tribunais_estao_arquivadas, False)
        self.assertTrue(bool(processo.match_fontes))
        self.assertTrue(processo.match_fontes.tribunal)
        self.assertFalse(processo.match_fontes.diario_oficial)
        self.assertEqual(len(processo.fontes), 1)

        # FONTE
        fonte = processo.fontes[0]
        self.assertEqual(fonte.id, 15399)
        self.assertEqual(fonte.processo_fonte_id, 222514338)
        self.assertEqual(fonte.descricao, "TRF1 - 1º grau")
        self.assertEqual(fonte.nome, "Tribunal Regional Federal da 1ª Região")
        self.assertEqual(fonte.sigla, "TRF1")
        self.assertEqual(fonte.tipo, "TRIBUNAL")
        self.assertEqual(fonte.data_inicio, "2023-04-01")
        self.assertEqual(fonte.data_ultima_movimentacao, "2023-04-01")
        self.assertEqual(fonte.segredo_justica, None)
        self.assertEqual(fonte.arquivado, None)
        self.assertEqual(fonte.status_predito, "ATIVO")
        self.assertEqual(fonte.grau, 1)
        self.assertEqual(fonte.sistema, "PJE")
        self.assertEqual(
            fonte.url,
            "https://pje1g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam",
        )
        self.assertEqual(fonte.quantidade_movimentacoes, 1)
        self.assertEqual(fonte.quantidade_envolvidos, 1)
        self.assertEqual(fonte.data_ultima_verificacao, "2023-04-01T13:45:30+00:00")
        self.assertEqual(fonte.match_documento_por, "DOCUMENTO_TRIBUNAL")
        self.assertEqual(len(fonte.envolvidos), 1)

        # TIPOS ENVOLVIDO PESQUISADO
        self.assertEqual(len(fonte.tipos_envolvido_pesquisado), 2)
        self.assertEqual(fonte.tipos_envolvido_pesquisado[0].id, 3185)
        self.assertEqual(fonte.tipos_envolvido_pesquisado[0].tipo, "Autoridade")
        self.assertEqual(fonte.tipos_envolvido_pesquisado[0].tipo_normalizado, "Autoridade")
        self.assertEqual(fonte.tipos_envolvido_pesquisado[0].polo, "ATIVO")
        self.assertEqual(fonte.tipos_envolvido_pesquisado[1].id, 346)
        self.assertEqual(fonte.tipos_envolvido_pesquisado[1].tipo, "autor do Fato")
        self.assertEqual(fonte.tipos_envolvido_pesquisado[1].tipo_normalizado, "Réu")
        self.assertEqual(fonte.tipos_envolvido_pesquisado[1].polo, "PASSIVO")


        # CAPA
        self.assertEqual(fonte.capa.classe, "AUTO DE PRISAO EM FLAGRANTE")
        self.assertEqual(fonte.capa.assunto, "CRIMES CONTRA A ORDEM ECONOMICA")
        self.assertEqual(fonte.capa.area, None)
        self.assertEqual(fonte.capa.orgao_julgador, "4ª VARA FEDERAL CRIMINAL DA SJRR")
        self.assertEqual(fonte.capa.data_distribuicao, "2023-04-01")
        self.assertEqual(fonte.capa.data_arquivamento, None)
        self.assertEqual(fonte.capa.informacoes_complementares, [])

        self.assertEqual(len(fonte.capa.assuntos_normalizados), 2)

        # CAPA -> ASSUNTO PRINCIPAL NORMALIZADO
        self.assertEqual(fonte.capa.assunto_principal_normalizado.id, 2027)
        self.assertEqual(
            fonte.capa.assunto_principal_normalizado.nome,
            "Crimes contra a Ordem Econômica",
        )
        self.assertEqual(
            fonte.capa.assunto_principal_normalizado.nome_com_pai,
            "Crimes Previstos na Legislação Extravagante > Crimes contra a Ordem Econômica",
        )
        self.assertEqual(
            fonte.capa.assunto_principal_normalizado.path_completo,
            "DIREITO PENAL > Crimes Previstos na Legislação Extravagante > Crimes contra a Ordem Econômica",
        )

        # CAPA -> VALOR CAUSA
        self.assertEqual(fonte.capa.valor_causa, None)

        # TRIBUNAL
        self.assertEqual(fonte.tribunal.id, 5)
        self.assertEqual(fonte.tribunal.sigla, "TRF1")
        self.assertEqual(fonte.tribunal.nome, "Tribunal Regional Federal da 1ª Região")
        self.assertEqual(fonte.tribunal.categoria, None)


if __name__ == "__main__":
    unittest.main()
