## SDK em python para utilizar a API do Escavador

### Instalação
    
Instale utilizando o pip:
```bash
pip install escavador
```

### Como Configurar

- Crie no `.env` do seu projeto uma variável `ESCAVADOR_API_KEY` com seu token da API
- ou
- utilize a função `config()`
```py
import escavador
escavador.config("API_KEY")
```

- para obter seu token da API, acesse o [painel de tokens](https://api.escavador.com/tokens)

### Exemplo de como utilizar
[Buscando informações do processo no sistema do Tribunal](https://api.escavador.com/docs/#pesquisar-processo-no-site-do-tribunal-assncrono) (Assíncrono)
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

### Criando Monitoramentos
```py
from escavador import MonitoramentoTribunal, MonitoramentoDiario, TiposMonitoramentosTribunal, TiposMonitoramentosDiario,FrequenciaMonitoramentoTribunal

# Monitoramento nos sisteams dos Tribunais
monitoramento_tribunal = MonitoramentoTribunal().criar(tipo_monitoramento=TiposMonitoramentosTribunal.UNICO,
                                                                     valor="8809061-58.2022.8.10.3695",tribunal='TJSP', 
                                                                     frequencia=FrequenciaMonitoramentoTribunal.SEMANAL)

# Monitoramento em Diários Oficiais
monitoramento_diario = MonitoramentoDiario().criar(TiposMonitoramentosDiario.PROCESSO, processo_id=2, origens_ids=[2,4,6])
```

### Consultando os Tribunais e sistemas disponíveis
```py
from escavador import Tribunal

tribunais_disponiveis = Tribunal().sistemas_disponiveis()
```

### Módulos Disponíveis e Referência da API

| Módulo                | Link API                                                          |
|-----------------------|-------------------------------------------------------------------|
| Busca                 | https://api.escavador.com/docs/#busca                             |
| Processo              | https://api.escavador.com/docs/#processos                         |
| Callback              | https://api.escavador.com/docs/#callback                          |
| DiarioOficial         | https://api.escavador.com/docs/#dirios-oficiais                   |
| Instituicao           | https://api.escavador.com/docs/#instituies                        |
| Legislacao            | https://api.escavador.com/docs/#legislao                          |
| Jurisprudencia        | https://api.escavador.com/docs/#jurisprudncias                    |
| MonitoramentoDiario   | https://api.escavador.com/docs/#monitoramento-de-dirios-oficiais  |
| MonitoramentoTribunal | https://api.escavador.com/docs/#monitoramento-no-site-do-tribunal |
| Movimentacao          | https://api.escavador.com/docs/#movimentaes                       |
| Pessoa                | https://api.escavador.com/docs/#pessoas                           |
| Tribunal              | https://api.escavador.com/docs/#tribunais                         |
| Saldo                 | https://api.escavador.com/docs/#saldo-da-api                      | 