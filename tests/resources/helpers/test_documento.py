from random import randint
import unittest
from escavador.resources.helpers.documento import Documento
from tempfile import NamedTemporaryFile


class TestDocumento(unittest.TestCase):
    def test_get_pdf(self):
        content = b"".join([bytes(chr(randint(0, 50000)), "utf-8") for i in range(100000)])
        with NamedTemporaryFile("wb") as temp:
            name = temp.name.split("\\")[-1]
            path = "\\".join(temp.name.split("\\")[:-1])
            realpath = Documento.get_pdf(
                content,
                path,
                name
            )["path"]
            self.assertEqual(str(realpath), temp.name+'.pdf')
            with open(realpath, "rb") as temp2:
                self.assertEqual(
                    temp2.read(),
                    content
                )

            erro = Documento.get_pdf(
                content,
                path,
                name
            )["error"]
            self.assertEqual(erro, "File exists")


if __name__ == "__main__":
    unittest.main()
