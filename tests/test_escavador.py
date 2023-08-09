import unittest


class TestEscavador(unittest.TestCase):
    def test_import_works(self):
        import escavador
        from escavador import v1, v2, resources


if __name__ == '__main__':
    unittest.main()
