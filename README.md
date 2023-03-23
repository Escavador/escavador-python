# O SDK em Python da API do Escavador

## Instalação
    
O SDK pode ser instalado via `pip` através do comando:
```bash
python -m pip install escavador
```

## Como Configurar

No arquivo `.env` na raíz do seu projeto, crie uma variável chamada `ESCAVADOR_API_KEY` e atribua a ela o seu token da API.

Alternativamente, utilize a função `config()` durante a execução do seu projeto, antes de utilizar qualquer outro módulo do SDK.
```py
import escavador
escavador.config("API_KEY")
```

Para obter seu token da API, acesse o [painel de tokens](https://api.escavador.com/tokens)

## Exemplos

### Buscando um processo assíncronamente usando a API V1
[Buscando informações do processo no sistema do Tribunal](https://api.escavador.com/v1/docs/#pesquisar-processo-no-site-do-tribunal-assncrono) (Assíncrono)
```py
from escavador import Processo, BuscaAssincrona
import time

resultado_busca = Processo().informacoes_no_tribunal("0078700-86.2008.5.17.0009")  # Gera uma busca assíncrona

while resultado_busca['resposta']['status'] == 'PENDENTE':
    # Aguarda para checar novamente
    print("Está pendente")
    time.sleep(20)

    id_async = resultado_busca['resposta']['id']
    resultado_busca = BuscaAssincrona().por_id(id_async)

# Checa a saida do processso
if resultado_busca['resposta']['status'] == 'ERRO':
    print("Deu erro, tentar novamente")
    exit(0)

if resultado_busca['resposta']['status'] == 'SUCESSO':
    busca_async = resultado_busca['resposta']
    for instancia in busca_async['resposta']['instancias']:
        print(instancia['assunto'])  # Imprime os assuntos das instâncias do processo
```

### Buscando as movimentações de um processo usando a API V2

```py
from escavador import SiglaTribunal
from escavador.v2 import BuscaProcesso


busca = BuscaProcesso().movimentacoes(numero_processo="0078700-86.2008.5.17.0009", tribunais=[SiglaTribunal.TJPE], qtd=100)

if busca['success']:
    for movimentacao in busca['resposta']['itens']:
        print(f"{movimentacao['data']} - {movimentacao['tipo']}:")
        print(f"{movimentacao['conteudo']}")
```

### Criando Monitoramentos na API V1
```py
from escavador import MonitoramentoTribunal, MonitoramentoDiario, TiposMonitoramentosTribunal, TiposMonitoramentosDiario,FrequenciaMonitoramentoTribunal

# Monitoramento nos sisteams dos Tribunais
monitoramento_tribunal = MonitoramentoTribunal().criar(tipo_monitoramento=TiposMonitoramentosTribunal.UNICO,
                                                                     valor="8809061-58.2022.8.10.3695",tribunal='TJSP', 
                                                                     frequencia=FrequenciaMonitoramentoTribunal.SEMANAL)

# Monitoramento em Diários Oficiais
monitoramento_diario = MonitoramentoDiario().criar(TiposMonitoramentosDiario.PROCESSO, processo_id=2, origens_ids=[2,4,6])
```

### Consultando os Tribunais e sistemas disponíveis para a API V1
```py
from escavador import Tribunal

tribunais_disponiveis = Tribunal().sistemas_disponiveis()
```

### Módulos Disponíveis e Referência da API

| Módulo                | Link API                                                             |
|-----------------------|----------------------------------------------------------------------|
| Busca                 | https://api.escavador.com/v1/docs/#busca                             |
| Processo              | https://api.escavador.com/v1/docs/#processos                         |
| Callback              | https://api.escavador.com/v1/docs/#callback                          |
| DiarioOficial         | https://api.escavador.com/v1/docs/#dirios-oficiais                   |
| Instituicao           | https://api.escavador.com/v1/docs/#instituies                        |
| Legislacao            | https://api.escavador.com/v1/docs/#legislao                          |
| Jurisprudencia        | https://api.escavador.com/v1/docs/#jurisprudncias                    |
| MonitoramentoDiario   | https://api.escavador.com/v1/docs/#monitoramento-de-dirios-oficiais  |
| MonitoramentoTribunal | https://api.escavador.com/v1/docs/#monitoramento-no-site-do-tribunal |
| Movimentacao          | https://api.escavador.com/v1/docs/#movimentaes                       |
| Pessoa                | https://api.escavador.com/v1/docs/#pessoas                           |
| Tribunal              | https://api.escavador.com/v1/docs/#tribunais                         |
| Saldo                 | https://api.escavador.com/v1/docs/#saldo-da-api                      | 
| v2.BuscaProcesso      | https://api.escavador.com/v2/docs/#processos                         |