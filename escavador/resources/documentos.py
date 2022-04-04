class Documento(object):

    @staticmethod
    def get_pdf(conteudo, path, nome_arquivo):
        """
        Salva um pdf vindo de respostas da API com o nome enviado, no diretório informado
        :param nome_arquivo: nome do arquivo a ser criado
        :param conteudo: pdf vindo de respostas da API
        :param path: caminho onde o pdf será salvo
        :return: json
        """
        path = f"{path}/{nome_arquivo}.pdf"

        try:
            open(path, "x")

            arquivo = open(path, "+wb")
            arquivo.write(conteudo)
            arquivo.close()
        except FileExistsError as error:
            return {"error": error.strerror}
        except FileNotFoundError as error:
            return {"error": error.strerror}

        return {"path": path}
