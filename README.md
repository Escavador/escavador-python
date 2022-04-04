## escavador-python
SDK em python para utilizar a API do Escavador

### Como Configurar

- Crie no `.env` do seu projeto uma variável `ESCAVADOR_API_KEY` com seu token da API
- para obter seu token da API, acesse o [painel de tokens](https://api.escavador.com/tokens)

### Como Utilizar
```py
from escavador import BuscaAssincrona

resultado_busca = BuscaAssincrona().get_processo("8809061-58.2022.8.10.3695")
```

### Módulos Disponíveis

| Módulo                | Link API                                                                          |
|-----------------------|-----------------------------------------------------------------------------------|
| Busca                 | https://api.escavador.com/docs/#busca & https://api.escavador.com/docs/#processos |
| BuscaAssincrona       | https://api.escavador.com/docs/#processos & https://api.escavador.com/docs/#busca |
| Callback              | https://api.escavador.com/docs/#callback                                          |
| DiarioOficial         | https://api.escavador.com/docs/#dirios-oficiais                                   |
| Instituicao           | https://api.escavador.com/docs/#instituies                                        |
| Legislacao            | https://api.escavador.com/docs/#legislao                                          |
| Jurisprudencia        | https://api.escavador.com/docs/#jurisprudncias                                    |
| Jurisprudencia        | https://api.escavador.com/docs/#jurisprudncias                                    |
| MonitoramentoDiario   | https://api.escavador.com/docs/#monitoramento-de-dirios-oficiais                  |
| MonitoramentoTribunal | https://api.escavador.com/docs/#monitoramento-no-site-do-tribunal                 |
| Movimentacao          | https://api.escavador.com/docs/#movimentaes                                       |
| Pessoa                | https://api.escavador.com/docs/#pessoas                                           |
| Tribunal              | https://api.escavador.com/docs/#tribunais                                         |
| Saldo                 | https://api.escavador.com/docs/#saldo-da-api                                      | 